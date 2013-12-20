import MySQLdb
import time
MySQLdb.paramstyle
from datetime import datetime
import fcntl
import time
import sys
     
def create_visit_type(ip_address, port1, username, password, database, values, identifier_type):
    port1 = int(port1)
    connMRS = MySQLdb.connect (host = ip_address,
        port=port1,
        user=username,
        passwd = password,
        db=database)
    # Map ids values of OpenERP to OpenMRS table

    
    name = values['name']
    description = values['description']
    
    date_created = values['date_created']
    for item in values:
        if (values[item] is None) or (values[item] is False):
            values[item] = "_"
    
    #insert on visit_type table
    cursoromrs1 = connMRS.cursor()
    
    insertvisittypestmt = """INSERT INTO visit_type(name,description,creator,date_created,uuid) VALUES(%s, %s,'1',now(), uuid())"""
    cursoromrs1.execute(insertvisittypestmt, (name, description))
    visit_type_id = int(cursoromrs1.lastrowid)
    cursoromrs1.execute("commit")
    cursoromrs1.close()
    
   
    return visit_type_id

def update_visit_type(ip_address, port1, username, password, database, values, identifier_type, visit_type_id):
    port1 = int(port1)
    connMRS = MySQLdb.connect (host = ip_address,
        port=port1,
        user=username,
        passwd = password,
        db=database)
    # Map ids values of OpenERP to OpenMRS table

    
    name = values['name']
    descrption = values['description']
    
    date_created = values['date_created']

    for item in values:
        if (values[item] is None) or (values[item] is False):
            values[item] = "_"

    #insert on visit_type table
    cursoromrs1 = connMRS.cursor()
    updatevisittypestmt = """UPDATE visit_type SET name = %s,description = %s,changed_by=1,date_changed = %s \
                  WHERE visit_type_id =  %s"""
    cursoromrs1.execute(updatevisittypestmt, (name, description, date_created,visit_type_id))
    visit_type_id = int(cursoromrs1.lastrowid)
    cursoromrs1.execute("commit")
    cursoromrs1.close()




def write_visit(ip_address, port1, username, password, database, values, identifier_type):
    port1 = int(port1)
    connMRS = MySQLdb.connect (host = ip_address,
        port=port1,
        user=username,
        passwd = password,
        db=database)
    # Map ids values of OpenERP to OpenMRS table

    
    visit_type = values['visit_type']
    visit_date = values['visit_date']
    patient = values['patient']
    
    date_created = values['date_created']


    for item in values:
        if (values[item] is None) or (values[item] is False):
            values[item] = "_"

    #insert on visit_type table
    cursoromrs1 = connMRS.cursor()
    insertvisitstmt = """INSERT INTO visit(patient_id,visit_type_id,date_started,creator,date_created,\
                  uuid) \
                  VALUES(%s, %s, %s,'1',%s, uuid())"""
    cursoromrs1.execute(insertvisitstmt, (patient, visit_type, visit_date,date_created))
    visit_id = int(cursoromrs1.lastrowid)
    cursoromrs1.execute("commit")
    cursoromrs1.close()
    return visit_id 


def update_visit(ip_address, port1, username, password, database, visit_id, values, identifier_type):
    port1 = int(port1)
    connMRS = MySQLdb.connect (host = ip_address,
        port=port1,
        user=username,
        passwd = password,
        db=database)
    # Map ids values of OpenERP to OpenMRS table

    
    visit_type = values['visit_type']
    visit_date = values['visit_date']
    patient = values['patient']
    
    date_created = values['date_created']


    for item in values:
        if (values[item] is None) or (values[item] is False):
            values[item] = "_"

    #insert on visit_type table
    cursoromrs1 = connMRS.cursor()
    insertvisitstmt = """UPDATE visit SET patient_id = %s ,visit_type_id = %s,date_started = %s,creator,date_created = %s \
                  WHERE visit_id = %s
                  VALUES(%s, %s, %s,'1',%s)"""
    cursoromrs1.execute(insertvisitstmt, (patient, visit_type, visit_date,date_created,visit_id))
    visit_id = int(cursoromrs1.lastrowid)
    cursoromrs1.execute("commit")
    cursoromrs1.close()

    
