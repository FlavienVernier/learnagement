
import os
import sys
import traceback

import dotenv
import mysql.connector

dotenv.load_dotenv(".env")

HOST=os.getenv("MYSQL_SERVER")
USER=os.getenv("MYSQL_USER_LOGIN")
PASSWORD=os.getenv("MYSQL_USER_PASSWORD")
DATABASE=os.getenv("MYSQL_DB")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



requests = {"check": {}, "struct": {}, "api": {}}

''' 
Return table without secndary key, that's prohibited by the framework
'''
requests["check"]["table_without_secondary_K"] = f"""
    SELECT DISTINCT `TABLE_NAME` 
    FROM `information_schema`.`KEY_COLUMN_USAGE`
    WHERE `TABLE_SCHEMA` =  '""" + os.getenv("MYSQL_DB") + """'
        and `TABLE_NAME` not in 
            (SELECT `TABLE_NAME` AS `TABLE_NAME`
            FROM `information_schema`.`KEY_COLUMN_USAGE`
            WHERE `TABLE_SCHEMA` = '""" + os.getenv("MYSQL_DB") + """'
                AND `CONSTRAINT_NAME` = 'SECONDARY');"""

''' 
Return table with error in there primary key name. 
According to the framework the table XXXX_name has id_name as primary key.
'''
requests["check"]["primaryK_namming_error"] = f"""
    SELECT DISTINCT TABLE_NAME, COLUMN_NAME, TRIM( SUBSTR(TABLE_NAME, LOCATE('_', TABLE_NAME)) ), TRIM( SUBSTR(COLUMN_NAME, LOCATE('_', COLUMN_NAME)) )
    FROM `information_schema`.`KEY_COLUMN_USAGE`
    WHERE `TABLE_SCHEMA` =  '""" + os.getenv("MYSQL_DB") + """'
        AND `CONSTRAINT_NAME` LIKE "PRIMARY"
        AND TABLE_NAME IN 
            (SELECT DISTINCT TABLE_NAME
            FROM `information_schema`.`KEY_COLUMN_USAGE`
            WHERE `TABLE_SCHEMA` =  '""" + os.getenv("MYSQL_DB") + """'
                AND `CONSTRAINT_NAME` LIKE "PRIMARY"
            GROUP BY TABLE_NAME
            HAVING COUNT(*)=1)
                AND TRIM( SUBSTR(TABLE_NAME, LOCATE('_', TABLE_NAME)) ) != TRIM( SUBSTR(COLUMN_NAME, LOCATE('_', COLUMN_NAME)) );"""

''' 
Return transition tables, according to the framwork table that primary keys are composed by 2 attributs
Note: these attributs can be checked if they are foreign keys 
'''
requests["struct"]["link_table"] = f"""
    SELECT `TABLE_NAME` AS `TABLE_NAME`
    FROM `information_schema`.`KEY_COLUMN_USAGE`
    WHERE `TABLE_SCHEMA` =  '""" + os.getenv("MYSQL_DB") + """'
        AND `CONSTRAINT_NAME` = 'PRIMARY'
    GROUP BY `TABLE_NAME`
    HAVING count(0) = 2;"""

''' 
Return linked table that are not transition tables
'''
requests["struct"]["linked_table"] = f"""
    SELECT DISTINCT `TABLE_NAME`
    FROM `information_schema`.`KEY_COLUMN_USAGE`
    WHERE `TABLE_SCHEMA` =  '""" + os.getenv("MYSQL_DB") + """'
        AND `CONSTRAINT_NAME` LIKE "FK%"
        AND `TABLE_NAME` NOT IN
            (SELECT `TABLE_NAME` AS `TABLE_NAME`
            FROM `information_schema`.`KEY_COLUMN_USAGE`
            WHERE `TABLE_SCHEMA` =  '""" + os.getenv("MYSQL_DB") + """'
                AND `CONSTRAINT_NAME` = 'PRIMARY'
            GROUP BY `TABLE_NAME`
            HAVING count(0) = 2);"""

''' 
Return leaf table: witout foreign keys
'''
requests["struct"]["leaf_table"] = f"""
    SELECT DISTINCT `TABLE_NAME` AS `TABLE_NAME`
    FROM `information_schema`.`KEY_COLUMN_USAGE`
    WHERE `TABLE_SCHEMA` =  '""" + os.getenv("MYSQL_DB") + """'
    AND `TABLE_NAME` NOT IN
        (SELECT `TABLE_NAME`
        FROM `information_schema`.`KEY_COLUMN_USAGE`
        WHERE `TABLE_SCHEMA` = 'learnagement'
            AND `CONSTRAINT_NAME` LIKE "FK%")"""

''' 
Return links from TABLE_NAME to REFFERENCED_TABLE_NAME
'''
requests["struct"]["link"] = f"""
    SELECT DISTINCT TABLE_NAME, REFERENCED_TABLE_NAME
    FROM `information_schema`.`KEY_COLUMN_USAGE`
    WHERE `TABLE_SCHEMA` =  '""" + os.getenv("MYSQL_DB") + """'
        AND `CONSTRAINT_NAME` LIKE "FK%";"""


requests["api"]["primary_key"] = f"""
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = '""" + os.getenv("MYSQL_DB") + """'
        AND COLUMN_KEY = 'PRI' 
        AND TABLE_NAME = %s
"""

requests["api"]["secondary_key"] = f"""
    
"""


def request(query, param=()):

    print("query/param: ", query, param, flush=True)

    conn = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
    )
    cursor = conn.cursor()
    try:
        cursor.execute(query, param)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Impossible d'exécuter la requête :", err)
        print(traceback.format_exc())
        return []
    finally:
        cursor.close()

    res = [row[0] for row in rows]
    return res

def get_primary_key_fields(conn, table_name):
    """

    """

    mysql_db = os.getenv("MYSQL_DB")

    query = f"""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = '{mysql_db}' 
          AND COLUMN_KEY = 'PRI' 
          AND TABLE_NAME = '{table_name}'
    """

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Impossible d'exécuter la requête :", err)
        print(traceback.format_exc())
        return []
    finally:
        cursor.close()

    primary_keys = [row[0] for row in rows]
    return primary_keys

def get_secondary_key_fields(conn, table_name):
    """

    """

    # get secondary key fields
    query = f"""
            SELECT column_name
            FROM information_schema.statistics
            WHERE table_schema =  '""" + os.getenv("MYSQL_DB") + """'
              AND table_name = '""" + table_name + """'
              AND INDEX_NAME = 'SECONDARY'
            """

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Impossible d'exécuter la requête :", err)
        print(traceback.format_exc())
        return []
    finally:
        cursor.close()

    secondary_keys_fields = [row[0] for row in rows]
    return secondary_keys_fields

def get_foreign_keys(conn, table_name):
    """

    """


    query = f"""
        SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, 
               REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_SCHEMA = '""" + os.getenv("MYSQL_DB") + """'
          AND TABLE_NAME = '""" + table_name + """'
    """
    #print("query", query, flush=True)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Impossible d'exécuter la requête : {err}")
        print(traceback.format_exc())
        return {}
    finally:
        cursor.close()

    # Build dictionary: FK column -> referenced table
    foreign_keys = {row[1]: row[3] for row in rows if row[3] is not None}
    return foreign_keys

def __build_secondary_key_request(conn, table):
    """

    """

    mysql_db = os.getenv("MYSQL_DB")

    cursor = conn.cursor()

    # get primary key fields
    primary_keys_fields = get_primary_key_fields(conn, table)
    #print("primary_keys_fields", primary_keys_fields, flush=True)

    # get foreign key fields (fonction à implémenter comme en PHP)
    foreign_keys_fields = get_foreign_keys(conn, table)
    #print("foreign_keys_fields", foreign_keys_fields, flush=True)

    # get secondary key fields
    secondary_keys_fields = get_secondary_key_fields(conn, table)
    #print("secondary_keys_fields", secondary_keys_fields, flush=True)

    # initial request dict
    request_as_dict = {
        "SELECT": [],
        "SELECT_PRIM": [f"{table}.{pk}" for pk in primary_keys_fields],
        "FROM": "",
        "MAINTABLE": table
    }

    # iterate over secondary keys
    for secondary_key_field in secondary_keys_fields:
        if secondary_key_field in foreign_keys_fields.keys():
            # recursive call
            sub_request = __build_secondary_key_request(conn, foreign_keys_fields[secondary_key_field])

            # merge SELECT and SELECT_PRIM
            request_as_dict["SELECT"].extend(sub_request["SELECT"])
            request_as_dict["SELECT_PRIM"].extend(sub_request["SELECT_PRIM"])

            # build FROM clause with join
            sub_table = sub_request["MAINTABLE"]
            sub_primary = get_primary_key_fields(conn, foreign_keys_fields[secondary_key_field])[0]
            request_as_dict["FROM"] += (
                f" JOIN {sub_table} ON {sub_table}.{sub_primary} = {table}.{secondary_key_field}"
                f"{sub_request['FROM']}"
            )
        else:
            request_as_dict["SELECT"].append(f"{table}.{secondary_key_field}")

    return request_as_dict

def build_secondary_key_request(conn, table):
    # get first primary key field
    primary_key_field = get_primary_key_fields(conn, table)[0]
    #print("Primary key field: ", primary_key_field, flush=True)

    # build the recursive dictionary
    secondary_key_request_dict = __build_secondary_key_request(conn, table)
    #print("Secondary key request dict: ", secondary_key_request_dict, flush=True)

    # convert list fields to string for SQL
    select_fields = ", ".join(secondary_key_request_dict["SELECT"])
    select_prim_fields = ", ".join(secondary_key_request_dict["SELECT_PRIM"])
    from_clause = f"{table} {secondary_key_request_dict['FROM']}"

    # build the final SQL query
    secondary_key_request = f"""
        CREATE OR REPLACE VIEW ExplicitSecondaryKs_{table} AS
        SELECT {primary_key_field} AS id,
               CONCAT_WS(' ', {select_fields}) AS ExplicitSecondaryK,
               {select_prim_fields}
        FROM {from_clause}
    """

    return secondary_key_request

if __name__ == '__main__':

    conn = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
    )

    print("##############################################################", flush=True)
    tables = request(requests["check"]["table_without_secondary_K"])
    for table in tables:
        print(bcolors.WARNING + "Warning: " + table + " has no secondary key!" + bcolors.ENDC)

    tables = request(requests["check"]["primaryK_namming_error"])
    for table in tables:
        print(bcolors.WARNING + "Warning: " + table + " has wrong primary key naming!" + bcolors.ENDC)

    tables = request(requests["struct"]["linked_table"])
    #print("Tables: ", tables, flush=True)
    #print("Table", build_secondary_key_request(conn, tables[0]), flush=True)

    for table in tables:
        query = build_secondary_key_request(conn, table)
        #print("Table", query, flush=True)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Impossible d'exécuter la requête \n {query}:\n {err}")
            print(traceback.format_exc())
        finally:
            cursor.close()

    conn.close()