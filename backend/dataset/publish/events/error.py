import csv
import logging
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
                         "serviceRequestNumber": error["serviceRequestNumber"],
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
        error_record = self.get_error_report(data["serviceRequestNumber"])
        try:
            if error_record:
                error_record = error_record[0]
                file = error_record["file"]
                if "eof" in data.keys():
                    if 'tool' in data.keys():
                        if data["eof"] and data["tool"] == pt_publish_tool:
                            path = file.split("/")[2]
                            aws_file = utils.upload_file(file, f'{aws_error_prefix}{path}')
                            if aws_file:
                                error_record["status"] = pt_success_status
                                error_record["file"] = aws_file
                                error_record["lastModifiedTime"] = str(datetime.now())
                                error_record["endTime"] = error_record["lastModifiedTime"]
                                error_repo.update(error_record)
                            return
                if error_record["status"] == pt_inprogress_status:
                    self.write_to_csv(data, file, False)
                    error_record["lastModifiedTime"] = str(datetime.now())
                    error_repo.update(error_record)
            else:
                if "eof" not in data.keys():
                    file = f'{shared_storage_path}error-{data["serviceRequestNumber"]}.csv'
                    self.write_to_csv(data, file, True)
                    error_rec = {"id": str(uuid.uuid4()), "serviceRequestNumber": data["serviceRequestNumber"], "status": pt_inprogress_status,
                             "file": file, "startTime": str(datetime.now()), "lastModifiedTime": str(datetime.now())}
                    error_repo.insert(error_rec)
        except Exception as e:
            log.exception(f'Exception while writing errors: {e}', e)
            return

    def write_to_csv(self, data, file, create):
        data_file = open(file, 'w')
        csv_writer = csv.writer(file)
        if create:
            header = data.keys()
            csv_writer.writerow(header)
        csv_writer.writerow(data.values())
        data_file.close()

    def get_error_report(self, srn):
        query = {"serviceRequestNumber": srn}
        exclude = {"_id", False}
        error_record = error_repo.search(query, exclude, None, None)
        if error_record:
            return error_record
        else:
            return []


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