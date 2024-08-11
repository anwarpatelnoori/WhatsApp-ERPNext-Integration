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
    current_minute = datetime.now().minute
    if today <= formated_end_date:
        day_remainig = frappe.utils.date_diff(formated_end_date, today)
        if current_hour== 0 and current_minute == 0:
            joke = frappe.db.get_value('Joke',filters={'am_pm':'AM','avail':1},fieldname='joke')
            joke_name = frappe.db.get_value('Joke',filters={'am_pm':'AM','avail':1},fieldname='name')
            if joke:
                message = f"""Hi, Mohammed Zulfekhar Ahmed, I know you are counting the days on your fingertips, don't waste your time on that😂😂😂. So {day_remainig} days to go from now.\n\nHave a Smile for a while😜\n\n{joke}\n\n An automated message til {end_date}🤓🤓"""
                send_whatsapp_without_pdf(message)
                frappe.db.set_value('Joke',joke_name,'avail',0)
        elif current_hour == 12 and current_minute == 0:
            joke = frappe.db.get_value('Joke',filters={'am_pm':'PM','avail':1},fieldname='joke')
            joke_name = frappe.db.get_value('Joke',filters={'am_pm':'PM','avail':1},fieldname='name')
            if joke:
                message = f"""Hi, Mohammed Zulfekhar Ahmed, I know you are counting the days on your fingertips, don't waste your time on that😂😂😂. So {day_remainig} days to go from now.\n\nSmile for this😜\n\n{joke}\n\n An automated message til {end_date}🤓🤓"""
                send_whatsapp_without_pdf(message)
                frappe.db.set_value('Joke',joke_name,'avail',0)
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
        frappe.log_error(title='Failed to send notification', message=frappe.get_traceback())  