# config.py

DEFAULT = {
    'RULE_LOG_TABLE_NAME': 'DQ2_RULE_LOG',
    'RULE_LOG_REF_TABLE_NAME': 'DQ2_RULE_LOG_REF',
    'RESULT_TABLE': 'DQ_RULE_LOG_RESULT'
    ,'TEST_RULE_SET_ASSIGNMENT': 'PAYPAL_PARTY_PARTY_COLUMNS_DQ_CHECK'  # Use just for testing, remove later

}

MYSQL_DATABASE_CONFIG = {
    'host': 'localhost',
    'dbname': 'dq_metadata_new',
    'user': 'root',
    'password': 'Cloudera',
    'port': '3306'
}


TEST_DB = {
    'DB_NAME' : 'DQ_METADATA_NEW'

}


EMAIL_CONFIG ={
    'To': 'rishikumar.tamrakar@clairvoyantsoft.com',
    'sub': 'Stats For DQ FrameWork Unit Testing'
}

SQL_QUERY = {
    'USE_DB': "USE {DB} ;",
    'TRUNCATE_SQL': "TRUNCATE TABLE {DB}.{TABLE} ; ",
    'TABLE_LOCK_SQL': "LOCK TABLES {DB}.{TABLE} WRITE;",
    'TABLE_UNLOCK_SQL': "UNLOCK TABLES ;",
    'COMMIT_SQL' : "COMMIT ;",

    'CREATE_RES_TBL':"""
    CREATE TABLE IF NOT EXISTS {DB}.{TABLE_NM} (
 `REC_NUM` int(50) NOT NULL auto_increment,
 `ID` varchar(500) COLLATE utf8_unicode_ci NOT NULL,
 `RULE_ASSIGNMENT_ID` INT,
 `RULE_SET_ASSIGNMENT_ID` INT,
 `RESULT` VARCHAR(45) NOT NULL,
 `REF_RESULT` VARCHAR(45) NOT NULL,
 `STATUS` VARCHAR(45) NOT NULL,
 `REF_STATUS` VARCHAR(45) NOT NULL,
 `TEST_RESULT` VARCHAR(45) NOT NULL,
 `CREATE_TS` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 `UPDATE_TS` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (`REC_NUM`)
);
    """,

    'RESULT_TESTING_SQL': """
INSERT INTO {DB}.{RESULT_TABLE}
(ID,RULE_ASSIGNMENT_ID,RULE_SET_ASSIGNMENT_ID,RESULT,REF_RESULT,STATUS,REF_STATUS,TEST_RESULT)
SELECT DQ.ID, DQ.RULE_ASSIGNMENT_ID, DQ.RULE_SET_ASSIGNMENT_ID, DQ.RESULT , REF.RESULT AS REF_RESULT, DQ.STATUS, REF.STATUS 
, CASE WHEN (DQ.RESULT = REF.RESULT) AND (DQ.STATUS = REF.STATUS) THEN 'PASS' ELSE 'FAIL' END AS TEST_RESULT  
FROM {DB}.{RULE_LOG_TABLE_NAME} DQ LEFT JOIN {DB}.{RULE_LOG_REF_TABLE_NAME} REF  
ON SUBSTR(DQ.ID,1,LENGTH(DQ.ID)-21) = SUBSTR(REF.ID,1,LENGTH(REF.ID)-21)
AND DQ.RULE_ASSIGNMENT_ID = REF.RULE_ASSIGNMENT_ID
AND DQ.RULE_SET_ASSIGNMENT_ID = REF.RULE_SET_ASSIGNMENT_ID ; 
""",

    'CREATE_IMAGE_TABLE': " CREATE TABLE {DB}.{NEW_TABLE} LIKE {DB}.{OLD_TABLE} ;" ,
    'COPY_TABLE_DATA': """ INSERT INTO {DB}.{TGT_TBL}
    SELECT * FROM {DB}.{SRC_TBL} ;"""
}

