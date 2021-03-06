# AUTOGENERATED! DO NOT EDIT! File to edit: 01_contacts.ipynb (unless otherwise specified).

__all__ = ['contact_exists', 'get_contact', 'get_contact_by_id', 'create_contact', 'delete_contact', 'create_contacts',
           'update_contact', 'create_or_update_contact']

# Cell
# export

import time
import os
import json
import requests
from dotenv import load_dotenv
from .search import hubspot_search
load_dotenv()

# Cell


def contact_exists(value, property='email', operator='EQ', hapikey=None) -> bool:
    """
    Check if a contact exists.
    """
    r = hubspot_search(value, property=property, operator=operator, hapikey=hapikey)
    if r.get('total',0) > 0:
        return True
    else:
        return False



# Cell


def get_contact(value, property='email', operator='EQ', hapikey=None, properties=None):
    """
    Get contact.
    """
    if hapikey is None:
        hapikey = os.environ.get('HUBSPOT_API_KEY','demo')
    r = hubspot_search(value, property=property, operator=operator, hapikey=hapikey, properties=properties)
    if 'total' in r:
        if r['total'] > 0:
            contact = r['results'][0]
            return contact
        else:
            return None
    else:
        return None



# Cell


def get_contact_by_id(id, hapikey=None, properties=None):
    """
    Get contact by id.
    """
    if hapikey is None:
        hapikey = os.environ.get('HUBSPOT_API_KEY','demo')
    endpoint = 'https://api.hubapi.com/crm/v3/objects/contacts/'
    url = f'{endpoint}/{id}'
    querystring = {"hapikey": hapikey, "properties": properties}
    headers = {"accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    return response



# Cell


def create_contact(contact=None, hapikey=None):
    """
    Create a contact.
    """
    if contact is None:
        contact = dict(email='sometestuser@example.com')
    if hapikey is None:
        hapikey = os.environ.get('HUBSPOT_API_KEY','demo')
    endpoint = 'https://api.hubapi.com/contacts/v1/contact/'
    url = f'{endpoint}?hapikey={hapikey}'
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({"properties": [{"property": k,"value": contact[k]} for k in contact]})
    r = requests.post(url=url, data=data, headers=headers)
    return r



# Cell


def delete_contact(vid=None, hapikey=None):
    """
    Delete a contact.
    """
    if hapikey is None:
        hapikey = os.environ.get('HUBSPOT_API_KEY','demo')
    endpoint = f'https://api.hubapi.com/contacts/v1/contact/vid/{vid}'
    url = f'{endpoint}?hapikey={hapikey}'
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.delete(url=url, headers=headers)
    return r



# Cell


def create_contacts(contacts=None, hapikey=None, check_exists=True):
    """
    Create contacts from a list of contacts.
    """
    if hapikey is None:
        hapikey = os.environ.get('HUBSPOT_API_KEY','demo')
    url = "https://api.hubapi.com/contacts/v1/contact/batch"
    querystring = {"hapikey": hapikey}
    headers = {"Content-Type": "application/json"}
    payload = []
    # loop over contacts and build payload to send
    for contact in contacts:
        email = contact["email"]
        payload.append({"email": email, "properties": [{"property": k,"value": contact[k]} for k in contact]})
    payload = json.dumps(payload)
    r = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    if r.status_code == 202:
        return True
    else:
        raise ValueError(f"batch contact creation failed status_code={r.status_code} reason={r.reason}")
        return False



# Cell


def update_contact(email, properties, hapikey=None):
    """
    Update a contact.
    """
    if hapikey is None:
        hapikey = os.environ.get('HUBSPOT_API_KEY','demo')
    if contact_exists(email):
        contact = get_contact(email)
        vid = contact['id']
        endpoint = 'https://api.hubapi.com/contacts/v1/contact/'
        url = f'{endpoint}/vid/{vid}/profile?hapikey={hapikey}'
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({"properties": [{"property": k,"value": properties[k]} for k in properties]})
        r = requests.post(url=url, data=data, headers=headers)
        return r
    else:
        return None



# Cell


def create_or_update_contact(email, properties, hapikey=None):
    """
    Create or update a contact.
    """
    if hapikey is None:
        hapikey = os.environ.get('HUBSPOT_API_KEY','demo')
    endpoint = 'https://api.hubapi.com/contacts/v1/contact/'
    url = f'{endpoint}/createOrUpdate/email/{email}?hapikey={hapikey}'
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({"properties": [{"property": k,"value": properties[k]} for k in properties]})
    r = requests.post(url=url, data=data, headers=headers)
    return r

