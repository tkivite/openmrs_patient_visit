import time
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import openerp
from openerp import pooler, tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
#from patient_connect1 import connect, connect_write
from connect_visit import create_visit_type, update_visit_type
import fcntl
import sys

class patient_visit_type(osv.osv):
    """ Type of Patient Visit """
    _name = "patient.visit.type"
    _description = "Patient Visit Type"

    def create(self, cr, uid, vals, context={}):
        openmrs_object = self.pool.get('openmrs.connect')
        recId = openmrs_object.search(cr, uid, [], offset=0, limit=1, order=None, context=None, count=False)[0]
        username = openmrs_object.browse(cr, uid, recId, context={}).username
        ip_address = openmrs_object.browse(cr, uid, recId, context={}).ip_address
        port = openmrs_object.browse(cr, uid, recId, context={}).port
        password = openmrs_object.browse(cr, uid, recId, context={}).password
        database = openmrs_object.browse(cr, uid, recId, context={}).database
        identifier_type = openmrs_object.browse(cr, uid, recId, context={}).identifier_type


        res = super(patient_visit_type, self).create(cr, uid, vals)
        
        values = {}
        values['name'] = self.browse(cr, uid, res, context={}).name
        values['description'] = self.browse(cr, uid, res, context={}).description
        values['date_created'] = self.browse(cr, uid, res, context={}).date_created
        
        for item in values:
            if (values[item] is None) or (values[item] is False):
                values[item] = " "
        #raise osv.except_osv(_('Expecting an Agency Code'),_('IP adress is: %s' % values))
       
        try:
            id_openmrs = create_visit_type(ip_address, port, username, password, database, values, identifier_type)
            
            super(patient_visit_type, self).write(cr, uid, res, {'openmrs_ref': id_openmrs}, context={})
            super(patient_visit_type, self).write(cr, uid, res, {'for_synchronization': False}, context={})
        except:
            super(patient_visit_type, self).write(cr, uid, res, {'for_synchronization': True}, context={})
        return res

    def write(self, cr, uid, ids, vals, context={}):
        res = super(patient_visit_type, self).write(cr, uid, ids, vals)
        openmrs_object = self.pool.get('openmrs.connect')
        recId = openmrs_object.search(cr, uid, [], offset=0, limit=1, order=None, context=None, count=False)[0]
        username = openmrs_object.browse(cr, uid, recId, context={}).username
        ip_address = openmrs_object.browse(cr, uid, recId, context={}).ip_address
        port = openmrs_object.browse(cr, uid, recId, context={}).port
        password = openmrs_object.browse(cr, uid, recId, context={}).password
        database = openmrs_object.browse(cr, uid, recId, context={}).database
        identifier_type = openmrs_object.browse(cr, uid, recId, context={}).identifier_type
        
        for rec in ids:
            values ={}
            values['name'] = self.browse(cr, uid, rec, context={}).name
            values['description'] = self.browse(cr, uid, rec, context={}).description
            values['date_created'] = self.browse(cr, uid, res, context={}).date_created
            #visit_type_id=1;    
            visit_type_id = self.browse(cr, uid, rec, context={}).openmrs_ref
            #raise osv.except_osv(_('Expecting an Agency Code'),_('IP adress is: %s' % patientid))
            for item in values:
                if (values[item] is None) or (values[item] is False):
                    values[item] = " "
            #raise osv.except_osv(_('Expecting an Agency Code'),_('ids numbers: %s' % ids))
            if visit_type_id != 0:
                try:
                    update_visit_type(ip_address, port, username, password, database, values, identifier_type, visit_type_id)
                    super(patient_visit_type, self).write(cr, uid, rec, {'for_synchronization': False}, context={})
                except:
                    super(patient_visit_type, self).write(cr, uid, rec, {'for_synchronization': True}, context={})
            else:
                try:
                    id_openmrs = create_visit_type(ip_address, port, username, password, database, values, identifier_type)
                    super(patient_visit_type, self).write(cr, uid, rec, {'openmrs_ref': id_openmrs}, context={})
                    super(patient_visit_type, self).write(cr, uid, rec, {'for_synchronization': False}, context={})

                except:
                    super(patient_visit_type, self).write(cr, uid, rec, {'for_synchronization': True}, context={})

        return True


    def synchronizeVtypes(self, cr, uid, *args):
        syncIds = self.pool.get('patient.visit.type').search(cr, uid, [('for_synchronization', '=', True)], offset=0, limit=None, order=None, context=None, count=False)
        self.pool.get('patient.visit.type').write(cr, uid, syncIds, {}, context={})
        raise osv.except_osv(_('Synchronization:'),_('Complete')) 


    _columns = {
        'name': fields.char('Type Name', size=64, required=True),
        'description': fields.char('Description', size=64, required=True),
        'openmrs_ref': fields.integer('Openmrs Number'),
        'for_synchronization': fields.boolean('For Synchronization'),
        'date_created': fields.datetime('Date Created'),
    }
    _sql_constraints = [
        ('name', 'unique(name)', 'The name of the visit type must be unique')
    ]
    _order = 'name asc'

    _defaults = {
        'date_created': lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  
     }   
patient_visit_type()

class patient_visit(osv.osv):
    """ Patient Visit """
    _name = "patient.visit"
    _description = "Patient Visit"
   
    
    def create(self, cr, uid, vals, context={}):
        openmrs_object = self.pool.get('openmrs.connect')
        recId = openmrs_object.search(cr, uid, [], offset=0, limit=1, order=None, context=None, count=False)[0]
        username = openmrs_object.browse(cr, uid, recId, context={}).username
        ip_address = openmrs_object.browse(cr, uid, recId, context={}).ip_address
        port = openmrs_object.browse(cr, uid, recId, context={}).port
        password = openmrs_object.browse(cr, uid, recId, context={}).password
        database = openmrs_object.browse(cr, uid, recId, context={}).database
        identifier_type = openmrs_object.browse(cr, uid, recId, context={}).identifier_type

        res = super(patient_visit, self).create(cr, uid, vals)

        values = {}
        values['patient'] = self.browse(cr, uid, res, context={}).patient
        values['visit_type'] = self.browse(cr, uid, res, context={}).visit_type
        values['visit_date'] = self.browse(cr, uid, res, context={}).date_of_visit
        values['date_created'] = self.browse(cr, uid, res, context={}).date_created
        
        
        for item in values:
            if (values[item] is None) or (values[item] is False):
                values[item] = " "
        #raise osv.except_osv(_('Expecting an Agency Code'),_('IP adress is: %s' % values))
        try:
            id_openmrs = create_visit(ip_address, port, username, password, database, values, identifier_type)
            super(patient_visit, self).write(cr, uid, res, {'openmrs_ref': id_openmrs}, context={})
            super(patient_visit, self).write(cr, uid, res, {'for_synchronization': False}, context={})
        except:
            super(patient_visit, self).write(cr, uid, res, {'for_synchronization': True}, context={})
        return res

    def write(self, cr, uid, ids, vals, context={}):
        res = super(patient_visit, self).write(cr, uid, ids, vals)
        openmrs_object = self.pool.get('openmrs.connect')
        recId = openmrs_object.search(cr, uid, [], offset=0, limit=1, order=None, context=None, count=False)[0]
        username = openmrs_object.browse(cr, uid, recId, context={}).username
        ip_address = openmrs_object.browse(cr, uid, recId, context={}).ip_address
        port = openmrs_object.browse(cr, uid, recId, context={}).port
        password = openmrs_object.browse(cr, uid, recId, context={}).password
        database = openmrs_object.browse(cr, uid, recId, context={}).database
        identifier_type = openmrs_object.browse(cr, uid, recId, context={}).identifier_type
        for rec in ids:
            values ={}
            values['patient'] = self.browse(cr, uid, rec, context={}).patient
            values['visit_type'] = self.browse(cr, uid, rec, context={}).visit_type
            values['visit_date'] = self.browse(cr, uid, rec, context={}).date_of_visit
            values['date_created'] = self.browse(cr, uid, res, context={}).date_created
            
                 
            visit_id = self.browse(cr, uid, rec, context={}).openmrs_ref
            #raise osv.except_osv(_('Expecting an Agency Code'),_('IP adress is: %s' % patientid))
            for item in values:
                if (values[item] is None) or (values[item] is False):
                    values[item] = " "
            #raise osv.except_osv(_('Expecting an Agency Code'),_('ids numbers: %s' % ids))
            if visit_id != 0:
                try:
                    update_visit(ip_address, port, username, password, database, visit_id, values, identifier_type)
                    super(patient_visit, self).write(cr, uid, rec, {'for_synchronization': False}, context={})
                except:
                    super(patient_visit, self).write(cr, uid, rec, {'for_synchronization': True}, context={})
            else:
                try:
                    id_openmrs = create_visit(ip_address, port, username, password, database, values, identifier_type)
                    super(patient_visit, self).write(cr, uid, rec, {'openmrs_ref': id_openmrs}, context={})
                    super(patient_visit, self).write(cr, uid, rec, {'for_synchronization': False}, context={})

                except:
                    super(patient_visit, self).write(cr, uid, rec, {'for_synchronization': True}, context={})

        return True


    def synchronizeVisits(self, cr, uid, *args):
        syncIds = self.pool.get('patient.visit').search(cr, uid, [('for_synchronization', '=', True)], offset=0, limit=None, order=None, context=None, count=False)
        self.pool.get('patient.visit').write(cr, uid, syncIds, {}, context={})
        raise osv.except_osv(_('Synchronization:'),_('Complete')) 





    _columns = {
        'visit_ref': fields.char('Visit Number', size=64, required=True), 
        'patient': fields.many2one('res.partner', 'Patient',required=True),
        'openmrs_ref': fields.integer('OpenMRS Reference'),
        'date_of_visit': fields.date('Date of Visit'),
        'visit_type': fields.many2one('patient.visit.type', 'Visit Type'),
        'visit_notes': fields.char('Notes', size=100),
        'for_synchronization': fields.boolean('For Synchronization'),
        'date_created': fields.datetime('Date Created'), 
    }
    _sql_constraints = [
        ('visit_ref', 'unique(visit_ref)', 'visit reference number must be unique')
    ]
    _order = 'date_of_visit desc'
    _defaults = {
        'visit_ref': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'visit.sequence.number'),
        'date_created': lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  
        'date_of_visit': lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  
    }
patient_visit()
