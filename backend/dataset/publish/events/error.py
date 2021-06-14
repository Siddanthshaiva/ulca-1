import csv
import json
import logging
import os
import uuid
from datetime import datetime
from logging.config import dictConfig
from configs.configs import error_event_input_topic, publish_error_code, shared_storage_path, pt_inprogress_status, \
    pt_success_status, aws_error_prefix, pt_publish_tool
from kafkawrapper.producer import Producer
from .errorrepo import ErrorRepo
from utils.datasetutils import DatasetUtils


log = logging.getLogger('file')
mongo_instance = None
prod = Producer()
error_repo = ErrorRepo()
utils = DatasetUtils()


class ErrorEvent:
    def __init__(self):
        pass

    def create_error_event(self, error_list):
        for error in error_list:
            log.info(f'Publishing error event for srn -- {error["serviceRequestNumber"]}')
            try:
                event = {"eventType": "dataset-training", "messageType": "error", "code": publish_error_code.replace("XXX", error["code"]),
                         "eventId": f'{error["serviceRequestNumber"]}|{str(uuid.uuid4())}', "timestamp": str(datetime.now()),
                         "serviceRequestNumber": error["serviceRequestNumber"], "stage": pt_publish_tool,
                         "datasetType": error["datasetType"], "message": error["message"], "record": error["record"]}
                if 'originalRecord' in error.keys():
                    event["originalRecord"] = error["originalRecord"]
                prod.produce(event, error_event_input_topic, None)
            except Exception as e:
                log.exception(e)
                continue

    def publish_eof(self, eof_event):
        log.info(f'Publishing EOF event to error for srn -- {eof_event["serviceRequestNumber"]}')
        eof_event["tool"] = pt_publish_tool
        prod.produce(eof_event, error_event_input_topic, None)

    def write_error(self, data):
        log.info(f'Writing error for SRN -- {data["serviceRequestNumber"]}')
        try:
            error_record = self.get_error_report(data["serviceRequestNumber"], True)
            if error_record:
                error_record = error_record[0]
                if 'eof' in data.keys():
                    if data["eof"]:
                        log.info(f'EOF received for SRN -- {data["serviceRequestNumber"]}')
                        error_record = self.upload_error_to_s3(error_record, data["serviceRequestNumber"])
                        error_record["status"] = pt_success_status
                        error_record["lastModifiedTime"] = str(datetime.now())
                        error_record["endTime"] = error_record["lastModifiedTime"]
                        error_record["error_list"] = None
                        error_repo.update(error_record)
                        return
                if error_record["status"] == pt_inprogress_status:
                    log.info(f'Updating error file for SRN -- {data["serviceRequestNumber"]}')
                    error_list = error_record["error_list"]
                    error_list.append(data)
                    error_record["error_list"] = error_list
                    error_record["lastModifiedTime"] = str(datetime.now())
                    error_repo.update(error_record)
            else:
                if "eof" not in data.keys():
                    log.info(f'Creating error file for SRN -- {data["serviceRequestNumber"]}')
                    file = f'{shared_storage_path}error-{data["serviceRequestNumber"]}.csv'
                    error_rec = {"id": str(uuid.uuid4()), "serviceRequestNumber": data["serviceRequestNumber"], "status": pt_inprogress_status,
                                 "internal_file": file, "file": file, "startTime": str(datetime.now()),
                                 "lastModifiedTime": str(datetime.now()), "error_list": [data]}
                    error_repo.insert(error_rec)
                else:
                    log.info(f'No errors for SRN -- {data["serviceRequestNumber"]}')
        except Exception as e:
            log.exception(f'Exception while writing errors: {e}', e)
            return

    def write_to_csv(self, data_list, file, srn):
        try:
            data_modified, data_pub = [], None
            for data in data_list:
                if isinstance(data, str):
                    data = json.loads(data)
                if 'stage' in data.keys():
                    if data["stage"] == pt_publish_tool:
                        data_pub = data
                data_modified.append(data)
            if not data_pub:
                data_pub = data_modified[0]
            with open(file, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, list(data_pub.keys()))
                dict_writer.writeheader()
                dict_writer.writerows(data_modified)
                output_file.close()
            log.info(f'{len(data_modified)} Errors written to csv for SRN -- {srn}')
            return
        except Exception as e:
            log.exception(f'Exception in csv writer: {e}', e)
            return

    def get_error_report(self, srn, internal):
        query = {"serviceRequestNumber": srn}
        exclude = {"_id": False}
        error_record = error_repo.search(query, exclude, None, None)
        if internal:
            return error_record
        try:
            if error_record:
                error_record = error_record[0]
                if error_record["status"] == pt_inprogress_status:
                    if error_record["error_list"]:
                        error_record = self.upload_error_to_s3(error_record, srn)
                    error_record["error_list"] = None
                return [error_record]
            else:
                return []
        except Exception as e:
            log.exception(f'Exception while fetching error report: {e}', e)
            return []

    def upload_error_to_s3(self, error_record, srn):
        file = error_record["internal_file"]
        path = file.split("/")[2]
        if error_record["file"] != file:
            utils.delete_from_s3(f'{aws_error_prefix}{path}')
        log.info(f'Error List: {len(error_record["error_list"])} for SRN -- {srn}')
        self.write_to_csv(error_record["error_list"], file, srn)
        error_record["file"] = utils.upload_file(file, f'{aws_error_prefix}{path}')
        error_repo.update(error_record)
        log.info(f'Error report uploaded to s3 for SRN -- {srn}')
        os.remove(file)
        return error_record

# Log config
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] {%(filename)s:%(lineno)d} %(threadName)s %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'info': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': 'info.log'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'file': {
            'level': 'DEBUG',
            'handlers': ['info', 'console'],
            'propagate': ''
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['info', 'console']
    }
})