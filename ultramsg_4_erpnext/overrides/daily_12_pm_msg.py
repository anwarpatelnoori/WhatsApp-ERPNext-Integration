import frappe
from datetime import datetime
from frappe import _
import requests
import time
import random


@frappe.whitelist()
def send_daily_whatsappmessage():
    end_date = '21/08/2024'
    formated_end_date = datetime.strptime(end_date, '%d/%m/%Y').date()  
    today = datetime.now().date()
    current_hour = datetime.now().hour
    current_datetime = datetime.now().replace(microsecond=0)
    nikah_datetime =   datetime.strptime('22/08/2024 12:00 PM', '%d/%m/%Y %I:%M %p')
    diff = nikah_datetime - current_datetime
    days = diff.days
    total_seconds = diff.seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    wait = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds" 
    if today <= formated_end_date:
        # joke = frappe.db.get_value('Joke',filters={'am_pm':'PM','avail':1,'date':today},fieldname='joke')
        # joke_name = frappe.db.get_value('Joke',filters={'am_pm':'PM','avail':1,'date':today},fieldname='name')

        joke = frappe.db.get_value('Joke',filters={'am_pm':'PM','avail':1},fieldname='joke')
        joke_name = frappe.db.get_value('Joke',filters={'am_pm':'PM','avail':1},fieldname='name')

        if joke:
            message = f"""Boooom Baaaam! 👏🏿👏🏿👏🏿, Mohammed Zulfekhar Ahmed, another 12hr is reduced 🥁🎷🎺🎹,.\n\n So {wait} remaining from now ⏳⌛.\n\nHave a Smile for a while😜\n\n{joke}\n\n An automated message til {end_date}🤓🤓"""
            send_whatsapp_without_pdf(message)
            frappe.db.set_value('Joke',joke_name,'avail',0)
        else:
            new_note = frappe.new_doc('Note')
            new_note.title = joke_name
            new_note.content = joke
            new_note.save()
    else:
        frappe.db.set_value('Server Script','Daily WhatsApp Message','disabled',1)
        frappe.db.commit

def send_whatsapp_without_pdf(message):
    token = frappe.get_doc('whatsapp message').get('token')
    message_url =  frappe.get_doc('whatsapp message').get('message_url')
    msg1 = message
    group_id = '120363324012320022@g.us'
    payload = {
        'token': token,
        'to':group_id,
        'body':msg1,
       }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    try:
        time.sleep(10)
        response = requests.post(message_url, data=payload, headers=headers)
        return response.text
    except Exception as e:
        current_hour = datetime.now().hour
        new_note = frappe.new_doc('Note')
        new_note.title = current_hour
        new_note.content = f"Failed to send message at this hour: {current_hour}"
        new_note.save()
        frappe.log_error(title='Failed to send notification', message=frappe.get_traceback())  