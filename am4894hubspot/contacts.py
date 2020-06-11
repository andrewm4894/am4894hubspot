# AUTOGENERATED! DO NOT EDIT! File to edit: 01_contacts.ipynb (unless otherwise specified).

__all__ = ['create_contact', 'contact_exists', 'get_contact', 'delete_contact', 'create_contacts']

# Cell
#export
import time
import os
import json
import requests
from dotenv import load_dotenv
from .search import hubspot_search
load_dotenv()

# Cell


def create_contact(contact=None, hapikey=None):
    """
    Create a contact.
    """
    if contact is None:
        contact = dict(email='sometestuser@example.com')
    if hapikey is None:
        hapikey = os.environ.get('HUBSPOT_API_KEY','demo')
    if not contact_exists(contact['email']):
        endpoint = 'https://api.hubapi.com/contacts/v1/contact/'
        url = f'{endpoint}?hapikey={hapikey}'
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({"properties": [{"property": k,"value": contact[k]} for k in contact]})
        r = requests.post(url=url, data=data, headers=headers)
        return r.json()
    else:
        return get_contact(contact['email'])

# Cell


def contact_exists(value, property='email', operator='EQ', hapikey=None) -> bool:
    """
    Check if a contact exists.
    """
    r = hubspot_search(value, property=property, operator=operator, hapikey=hapikey)
    if r['total'] > 0:
        return True
    else:
        return False

# Cell


def get_contact(value, property='email', operator='EQ', hapikey=None):
    """
    Get contact.
    """
    if hapikey is None:
        hapikey = os.environ.get('HUBSPOT_API_KEY','demo')
    r = hubspot_search(value, property=property, operator=operator, hapikey=hapikey)
    if r['total'] > 0:
        contact = r['results'][0]
        return contact
    else:
        return None

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
    return r.json()

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
        # only try create contacts not found
        email = contact["email"]
        if check_exists:
            # only append if does not exist
            if not contact_exists(email):
                payload.append({"email": email, "properties": [{"property": k,"value": contact[k]} for k in contact]})
            else:
                print(f"skipping {email} as already exists")
        else:
            payload.append({"email": email, "properties": [{"property": k,"value": contact[k]} for k in contact]})
    payload = json.dumps(payload)
    r = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    if r.status_code == 202:
        return True
    else:
        raise ValueError(f"batch contact creation failed status_code={r.status_code} reason={r.reason}")
        return False