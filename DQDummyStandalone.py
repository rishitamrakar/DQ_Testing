import pymysql
import conf.config  as config

def connect_db(db_name):
    conn = pymysql.connect(host=config.MYSQL_DATABASE_CONFIG['host'],
                           user=config.MYSQL_DATABASE_CONFIG['user'],
                           password=config.MYSQL_DATABASE_CONFIG['password'],
                           db=db_name)
    return conn


# Assigning Values to Variables
IN_RULE_SET_ASSIGNMENT = config.DEFAULT['TEST_RULE_SET_ASSIGNMENT']
DB_NAME = config.TEST_DB['DB_NAME']
RESULT_TABLE = config.DEFAULT['RESULT_TABLE']
RULE_LOG_TABLE_NAME = config.DEFAULT['RULE_LOG_TABLE_NAME']
RULE_LOG_REF_TABLE_NAME = config.DEFAULT['RULE_LOG_REF_TABLE_NAME']

# Creating db connection to mysql db
db = connect_db(DB_NAME)

cursor = db.cursor()
cursor.execute("truncate table DQ2_RULE_LOG ;")

cursor.execute(" insert into DQ_METADATA_NEW.DQ2_RULE_LOG select * from DQ_METADATA_NEW.dq2_rule_log_ref_dummy ;")
cursor.execute("commit ;")



# Closing db connection
db.close()