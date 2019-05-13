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

try:
    cursor.execute("select count(*) from {DB}.{TABLE} ;".format(DB=DB_NAME,TABLE=RULE_LOG_REF_TABLE_NAME))
    print ("Info : {DB}.{TABLE} already exists, ignoring Table creationg activity".format(DB=DB_NAME,TABLE=RULE_LOG_REF_TABLE_NAME))
except:
    print ("Info : {DB}.{TABLE} does not exists, creating table".format(DB=DB_NAME,TABLE=RULE_LOG_REF_TABLE_NAME))
    cursor.execute(config.SQL_QUERY['CREATE_IMAGE_TABLE'].format(DB=DB_NAME,NEW_TABLE=RULE_LOG_REF_TABLE_NAME,OLD_TABLE=RULE_LOG_TABLE_NAME))
    print ("Info : {DB}.{TABLE} Table created.".format(DB=DB_NAME,TABLE=RULE_LOG_REF_TABLE_NAME))

cursor.execute(config.SQL_QUERY['TRUNCATE_SQL'].format(DB=DB_NAME,TABLE=RULE_LOG_REF_TABLE_NAME))

cursor.execute(config.SQL_QUERY['COPY_TABLE_DATA'].format(DB=DB_NAME,SRC_TBL=RULE_LOG_TABLE_NAME,TGT_TBL=RULE_LOG_REF_TABLE_NAME))

cursor.execute(config.SQL_QUERY['COMMIT_SQL'])

cursor.execute(config.SQL_QUERY['TRUNCATE_SQL'].format(DB=DB_NAME,TABLE=RULE_LOG_TABLE_NAME))

db.close()