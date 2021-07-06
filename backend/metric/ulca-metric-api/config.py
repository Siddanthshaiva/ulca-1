import os
import time

DEBUG           = False
API_URL_PREFIX  = "/ulca/data-metric"
HOST            = '0.0.0.0'
PORT            = 5001
ENABLE_CORS     = False

# mongodb configs
MONGO_DB_SCHEMA         = os.environ.get('MONGO_DB_SCHEMA', 'test')
MONGO_CONNECTION_URL    = os.environ.get('MONGO_CLUSTER_URL', 'mongodb://localhost:27017')
#druid store configs
DRUID_DB_SCHEMA         = os.environ.get('MATRIC_DRUID_DB_SCHEMA', 'TEST4')
DRUID_CONNECTION_URL    = os.environ.get('DRUID_CLUSTER_URL', 'druid://localhost:8082/druid/v2/sql/')
#lang abbreviations
LANG_CODES        =    {'pa'        :'Punjabi', 
                        'bn'        :'Bengali',
                        'en'        :'English',
                        'ta'        :'Tamil', 
                        'ml'        :'Malayalam', 
                        'te'        :'Telugu', 
                        'kn'        :'Kannada', 
                        'hi'        :'Hindi', 
                        'mr'        :'Marathi',
                        'gu'        :'Gujarati',
                        'or'        :'Odia',
                        'as'        :'Assamese',
                        'kok'       :'Konkani',
                        'sa'        :'Sanskrit',
                        'ks'        :'Kashmiri',
                        'ne'        :'Nepali',
                        'ur'        :'Urdu',
                        'doi'       :'Dogri',
                        'mai'       :'Maithili',
                        'mni'       :'Manipuri',
                        'brx'       :'Bodo',
                        'sat'       :'Santali'  ,
                        'lus'       :'Lushai',
                        'njz'       :'Ngungwel',
                        'pnr'       :'Panim',
                        'kha'       :'Khasi',
                        'grt'       :'Garo'}