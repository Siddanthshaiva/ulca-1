
from .queryutils import QueryUtils
from config import DRUID_DB_SCHEMA , TIME_CONVERSION_VAL
import logging
from logging.config import dictConfig
log = logging.getLogger('file')


utils = QueryUtils()

class AggregateDatasetModel(object):
    def __init__(self):
        pass


    def data_aggregator(self, request_object):
        try:
            #query fields
            count   =   "count"
            total   =   "total"
            src     =   "sourceLanguage"
            tgt     =   "targetLanguage"
            delete  =   "isDelete"
            datatype=   "datasetType"  


            dtype = request_object["type"]
            if dtype in ["asr-corpus","asr-unlabeled-corpus"]:
                count = "durationInSeconds"
            match_params = None
            if "criterions" in request_object:
                match_params = request_object["criterions"]
            grpby_params = None
            if "groupby" in request_object:
                grpby_params = request_object["groupby"]

            sumtotal_query = f'SELECT SUM(\"{count}\") as {total},{delete}  FROM \"{DRUID_DB_SCHEMA}\"  WHERE ({datatype} = \'{dtype}\') GROUP BY {delete}'
            sumtotal_result = utils.query_runner(sumtotal_query)
            true_count = 0
            false_count = 0
            for val in sumtotal_result:
                if val[delete] == "false":
                    true_count = val[total]
                else:
                    false_count = val[total]
            sumtotal = true_count - false_count
            if dtype in ["asr-corpus","asr-unlabeled-corpus"]:
                sumtotal = sumtotal/TIME_CONVERSION_VAL

            #aggregate query for language pairs
            if grpby_params == None and len(match_params) ==1:
                query = f'SELECT SUM(\"{count}\") as {total}, {src}, {tgt},{delete} FROM \"{DRUID_DB_SCHEMA}\"'
                params = match_params[0]
                value = params["value"]

                if dtype == "parallel-corpus":
                    sub_query = f'WHERE (({datatype} = \'{dtype}\') AND ({src} != {tgt}) AND ({src} = \'{value}\' OR {tgt} = \'{value}\')) \
                                    GROUP BY {src}, {tgt},{delete}'

                elif dtype in ["asr-corpus","ocr-corpus","monolingual-corpus","asr-unlabeled-corpus"]:
                    sub_query = f'WHERE (({datatype} = \'{dtype}\')AND ({src} != {tgt})) GROUP BY {src}, {tgt},{delete}'
                qry_for_lang_pair  = query+sub_query

                result_parsed = utils.query_runner(qry_for_lang_pair)
                chart_data =  utils.result_formater_for_lang_pairs(result_parsed,dtype,value)

                return chart_data,sumtotal
            #aggregate query for groupby field
            if grpby_params != None and len(match_params) ==2:
                params = grpby_params[0]
                grp_field  = params["field"]
                src_val = next((item["value"] for item in match_params if item["field"] == "sourceLanguage"), False)
                tgt_val = next((item["value"] for item in match_params if item["field"] == "targetLanguage"), False)
                query = f'SELECT SUM(\"{count}\") as {total}, {src}, {tgt},{delete},{grp_field} FROM \"{DRUID_DB_SCHEMA}\"\
                            WHERE (({datatype} = \'{dtype}\') AND (({src} = \'{src_val}\' AND {tgt} = \'{tgt_val}\') OR ({src} = \'{tgt_val}\' AND {tgt} = \'{src_val}\')))\
                            GROUP BY {src}, {tgt}, {delete}, {grp_field}'

                result_parsed = utils.query_runner(query)
                chart_data = utils.result_formater(result_parsed,grp_field,dtype)
                return chart_data,sumtotal
            #aggregate query for groupby,matching
            if grpby_params != None and len(match_params) ==3:
                params = grpby_params[0]
                grp_field  = params["field"]
                if grp_field == "collectionMethod_collectionDescriptions":
                    sub_field = "domains"
                elif grp_field == "domains":
                    sub_field = "collectionMethod_collectionDescriptions"
                src_val = next((item["value"] for item in match_params if item["field"] == "sourceLanguage"), None)
                tgt_val = next((item["value"] for item in match_params if item["field"] == "targetLanguage"), None)
                sub_val = next((item["value"] for item in match_params  if item["field"] == None), None)
                query = f'SELECT SUM(\"{count}\") as {total}, {src}, {tgt},{delete},{grp_field} FROM \"{DRUID_DB_SCHEMA}\"\
                            WHERE (({datatype} = \'{dtype}\') AND (({src} = \'{src_val}\' AND {tgt} = \'{tgt_val}\') OR ({src} = \'{tgt_val}\' AND {tgt} = \'{src_val}\')))\
                            AND ({sub_field} = \'{sub_val}\') GROUP BY {src}, {tgt}, {delete}, {grp_field}'
                
                result_parsed = utils.query_runner(query)
                chart_data = utils.result_formater(result_parsed,grp_field,dtype)
                return chart_data,sumtotal
        except Exception as e:
            log.exception("Exception on query aggregation : {}".format(str(e)))
            return [],0

    

   


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