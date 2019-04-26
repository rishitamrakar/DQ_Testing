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
#cursor.execute("select count(*) from {TABLE_NAME} ;".format(TABLE_NAME=RESULT_TABLE))

cursor.execute("select count(*) from {DB}.{TABLE} where TEST_RESULT <> 'PASS';".format(DB=DB_NAME,TABLE=RESULT_TABLE))

row_count = (cursor.fetchone())[0]

print ("Info : Total number of Failed records : ",row_count)
cursor.execute("select REC_NUM, ID, TEST_RESULT from {DB}.{TABLE} where TEST_RESULT <> 'PASS';".format(DB=DB_NAME,TABLE=RESULT_TABLE))
a = cursor.description
print ("(",a[0][0],",",a[1][0],",",a[2][0],")")
rows = cursor.fetchall()

for row in rows:
    print (row)




db.close()

