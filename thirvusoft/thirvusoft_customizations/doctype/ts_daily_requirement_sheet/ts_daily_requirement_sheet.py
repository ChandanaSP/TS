# Copyright (c) 2022, ThirvuSoft Private Limited and contributors
# For license information, please see license.txt
 
 
from frappe.model.document import Document
 
class TSDailyRequirementSheet(Document):
   pass
 
import frappe
@frappe.whitelist()
def tech_lead_name_finder(ts_user,ts_value):
    ts_employee_user=frappe.db.get_values("Employee",filters={"user_id":ts_user},fieldname=["name",'employee_name',"designation"])
    if(ts_employee_user):
        ts_employee_user=ts_employee_user[0]
        ts_employee_user_id=ts_employee_user[0]
        ts_employee_user_name=ts_employee_user[1]
        ts_employee_user_name_designation=ts_employee_user[2]
        if(ts_value=="0"):
            if(ts_employee_user_name_designation=="Tech Lead"):
                return ts_employee_user_id,ts_employee_user_name
            else:
                return 1
        else:
            return ts_employee_user_id

 
 
from frappe.utils import getdate
from datetime import timedelta
@frappe.whitelist()
def employee_role(ts_user,ts_data):
   ts_data=eval(ts_data)
   ts_employee_user_id=frappe.db.get_values("Employee",filters={"user_id":ts_user},fieldname=["name",'employee_name',"designation"])
   if(ts_employee_user_id):
        ts_employee_user_id=ts_employee_user_id[0]
        if(ts_employee_user_id[2]=="Tech Lead"):
            ts_user_details=frappe.db.get_values("User",filters={"role_profile_name":"Scurm Master"},fieldname=["name"])
            if(ts_user_details):
                ts_user_details=ts_user_details[0]
                ts_scurm_user_details=frappe.db.get_values("Employee",filters={"user_id":ts_user_details[0]},fieldname=["name","employee_name"])
                ts_scurm_user_details=ts_scurm_user_details[0]
                ts_expected_start_date=getdate(ts_data["ts_expected_start_date"])
                ts_expected_end_date=ts_expected_start_date+timedelta(days=7)
                ts_new_task=frappe.get_doc({
                    "doctype":"Task",
                    "subject":ts_data["ts_subject"],
                    "project":ts_data["ts_project"],
                    "status":"Open",
                    "priority":ts_data["ts_priority"],
                    "assigned_tech_lead":ts_employee_user_id[0],
                    "assigned_ci":ts_data["ts_assigned_crm_member"],
                    "assigned_team_member":ts_data["ts_assigned_member"],
                    "ts_assigned_tech_lead_name":ts_employee_user_id[1],
                    "ts_assigned_ci_name":ts_data["ts_assigned_crm_name"],
                    "ts_assigned_team_member":ts_data["ts_assigned_member_name"],
                    "ts_scurm_master_id":ts_scurm_user_details[0],
                    "ts_scurm_master_name":ts_scurm_user_details[1],
                    "ts_scurm_master_mail":ts_user_details[0],
                    "exp_start_date":ts_data["ts_expected_start_date"],
                    "exp_end_date":ts_expected_end_date,
                    "expected_time":ts_data["ts_expected_hours"],
                    "description":ts_data["ts_requriement"],
                    "department":ts_data["ts_department"],
                })
                ts_new_task.insert()
                ts_new_task.save()
                return ts_employee_user_id[0],ts_employee_user_id[1]
            else:
                return 1
        
