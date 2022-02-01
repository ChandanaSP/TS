from __future__ import unicode_literals
import frappe
import unittest
from frappe.utils import random_string
from frappe.model.workflow import apply_workflow, WorkflowTransitionError, WorkflowPermissionError, get_common_transition_actions
from frappe.test_runner import make_test_records
from frappe.workflow.doctype.workflow.workflow import Workflow



def after_install():
	create_custom_role()
	create_custom_meeting()
	create_jobApplicant_workflow()



def create_custom_role():
	existing_doc = frappe.db.get_value('Role', {'role_name': 'Receptionist'}, 'name')
	if not existing_doc:
		new_doc = frappe.new_doc('Role')
		new_doc.role_name = 'Receptionist'
		new_doc.save()


def create_custom_meeting():
    meetlist=["General","Scrum","Management","Wonder","Thirvu","Client","Session"]
    for row in meetlist:
        new_doc = frappe.new_doc('TS Meeting Type')
        new_doc.ts_meeting_type = row
        new_doc.save()

def create_jobApplicant_workflow():
	if frappe.db.exists('Workflow', 'Job Applicant'):
		frappe.delete_doc('Workflow', 'Job Applicant')

	if not frappe.db.exists('Role', 'Receptionist'):
		frappe.get_doc(dict(doctype='Role',
			role_name='Receptionist')).insert(ignore_if_duplicate=True)
	workflow = frappe.new_doc('Workflow')
	workflow.workflow_name = 'Job Applicant workflow'
	workflow.document_type = 'Job Applicant'
	workflow.workflow_state_field = 'workflow_state'
	workflow.is_active = 1
	workflow.send_email_alert = 1
	workflow.append('states', dict(
		state = 'Draft', allow_edit = 'Receptionist',update_field = 'status', update_value = 'open'
	))
	workflow.append('states', dict(
		state = 'Applied', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Applied'
	))
	workflow.append('states', dict(
		state = 'Application Accepted', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Application Accepted'
	))
	workflow.append('states', dict(
		state = 'Application Rejected', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Application Rejected'
	))
	workflow.append('states', dict(
		state = 'Call for Interview', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Call for Interview'
	))
	workflow.append('states', dict(
		state = 'Invitation Accepted', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Invitation Accepted'
	))
	workflow.append('states', dict(
		state = 'Invitation Rejected', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Invitation Rejected'
	))
	workflow.append('states', dict(
		state = 'Initial Round', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Initial Round'
	))
	workflow.append('states', dict(
		state = 'Technical Round', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Technical Round'
	))
	workflow.append('states', dict(
		state = 'HR Round', allow_edit = 'Receptionist',update_field = 'status', update_value = 'HR Round'
	))
	workflow.append('states', dict(
		state = 'Document Verification', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Document Verification'
	))
	workflow.append('states', dict(
		state = 'Call Letter', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Call Letter'
	))
	workflow.append('states', dict(
		state = 'On Board', allow_edit = 'Receptionist',update_field = 'status', update_value = 'On Board'
	))
	workflow.append('states', dict(
		state = 'Rejected', allow_edit = 'Receptionist',update_field = 'status', update_value = 'Rejected'
	))
	workflow.append('transitions', dict(
		state = 'Draft', action='Applied', next_state = 'Applied',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Applied', action='Application Accepted', next_state = 'Application Accepted',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Applied', action='Reject', next_state = 'Draft',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Application Accepted', action='Call for Interview', next_state = 'Call for Interview',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Application Accepted', action='Reject', next_state = 'Draft',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Call for Interview', action='Invitation Accepted', next_state = 'Invitation Accepted',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Call for Interview', action='Reject', next_state = 'Invitation Rejected',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Invitation Accepted', action='Initial Round', next_state = 'Initial Round',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Invitation Accepted', action='Reject', next_state = 'Draft',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Initial Round', action='Technical Round', next_state = 'Technical Round',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Initial Round', action='Reject', next_state = 'Draft',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Technical Round', action='HR Round', next_state = 'HR Round',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Technical Round', action='Reject', next_state = 'Draft',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'HR Round', action='Document Verification', next_state = 'Document Verification',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'HR Round', action='Reject', next_state = 'Draft',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Document Verification', action='Call Letter', next_state = 'Call Letter',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Document Verification', action='Reject', next_state = 'Draft',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Call Letter', action='On Board', next_state = 'On Board',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.append('transitions', dict(
		state = 'Call Letter', action='Reject', next_state = 'Draft',
		allowed='Receptionist', allow_self_approval= 1
	))
	workflow.insert(ignore_permissions=True)

	return workflow