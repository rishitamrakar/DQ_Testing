import pymysql
import conf.config  as config


def connect_db(db_name):
    conn = pymysql.connect(host=config.MYSQL_DATABASE_CONFIG['host'],
                           user=config.MYSQL_DATABASE_CONFIG['user'],
                           password=config.MYSQL_DATABASE_CONFIG['password'],
                           db=db_name)
    return conn


# Assigning Value to  variables
IN_RULE_SET_ASSIGNMENT = 'PAYPAL_PARTY_PARTY_COLUMNS_DQ_CHECK'
DB_NAME = config.TEST_DB['DB_NAME']
RESULT_TABLE = config.DEFAULT['RESULT_TABLE']
RULE_LOG_TABLE_NAME = config.DEFAULT['RULE_LOG_TABLE_NAME']
RULE_LOG_REF_TABLE_NAME = config.DEFAULT['RULE_LOG_REF_TABLE_NAME']

# Creating db connection to mysql db
db = connect_db(DB_NAME)

cursor = db.cursor()

try:
    cursor.execute("select count(*) from {DB}.{TABLE_NM} ;".format(DB=DB_NAME,TABLE_NM=RESULT_TABLE))
    print ("Info : {DB}.{TABLE_NM} already exists, ignoring Table creation activity.".format(DB=DB_NAME,TABLE_NM=RESULT_TABLE))
except:
    print ("Info : {DB}.{TABLE_NM} does not exists, Creating Table.".format(DB=DB_NAME,TABLE_NM=RESULT_TABLE))
    cursor.execute(config.SQL_QUERY['CREATE_RES_TBL'].format(DB=DB_NAME,TABLE_NM=RESULT_TABLE))
    print ("Info : {DB}.{TABLE_NM} Created.".format(DB=DB_NAME,TABLE_NM=RESULT_TABLE))

cursor.execute(config.SQL_QUERY['TRUNCATE_SQL'].format(DB=DB_NAME,TABLE=RESULT_TABLE))
cursor.execute(config.SQL_QUERY['RESULT_TESTING_SQL'].format(DB=DB_NAME,RESULT_TABLE=RESULT_TABLE,RULE_LOG_TABLE_NAME=RULE_LOG_TABLE_NAME\
                                ,RULE_LOG_REF_TABLE_NAME=RULE_LOG_REF_TABLE_NAME,RULE_SET_ASSIGNMENT=IN_RULE_SET_ASSIGNMENT))
cursor.execute(config.SQL_QUERY['COMMIT_SQL'].format(DB=DB_NAME,TABLE=RESULT_TABLE))
cursor.execute(config.SQL_QUERY['TABLE_UNLOCK_SQL'].format(DB=DB_NAME,TABLEDB_NAME=RESULT_TABLE))

#Closing db connection
db.close()