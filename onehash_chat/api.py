import requests
import frappe
from frappe.utils.password import get_decrypted_password

ocs=frappe.get_doc('OneHash Chat Settings')
@frappe.whitelist(allow_guest=True)
def get_chatsettings():
    return ocs
    
if ocs.enabled:
    account_id = ocs.account_id
    fetch_contacts_en = ocs.auto_fetch_contacts
    source_token = get_decrypted_password('OneHash Chat Settings', ocs.name, 'access_token')
    base_url="https://chat.onehash.ai"
    inbox_id=ocs.inbox_id

    @frappe.whitelist()
    def fetch_contacts(): 
        if fetch_contacts_en:
            source_url = f"{base_url}/api/v1/accounts/{account_id}/contacts"
            source_headers = {
            'api_access_token': source_token
            }
            response = requests.get(source_url, headers=source_headers)

            if response.status_code == 200:
                data = response.json()
                contacts = data["payload"]
                
                for contact in contacts:
                    
                    full_name = contact["name"]
                    lead_email = contact["email"]
                    email_id = contact["email"]
                    phone = contact["phone_number"]
                    mobile_no = contact["phone_number"]
                    city = contact["additional_attributes"].get("city", "")
                    country = contact["additional_attributes"].get("country", "")
                    product = "OneHash Chat"
                    company_name = contact["additional_attributes"].get("company_name", "")
                    status = "Open"
                    
                    get_contacts=frappe.db.get_all('Contact',fields=['*'],filters={'email_id':email_id,'phone':phone})
                    
                    if not get_contacts:
                            l = frappe.get_doc(doctype='Lead', 
                            lead_name=full_name,
                            lead_email=lead_email,
                            email_id=email_id,
                            phone=phone,
                            mobile_no=mobile_no,
                            city=city,
                            country=country,
                            product=product,
                            company_name=company_name,
                            status=status)
                            l.insert()

    @frappe.whitelist()
    def post_contacts_to_chat():
        url = f"{base_url}/api/v1/accounts/{account_id}/contacts"

        get_contacts=frappe.db.get_list('Contact',fields=['*'])
        countcon=0            
        for i in get_contacts:
            email_id=i.email_id
            urlget = f"{base_url}/api/v1/accounts/{account_id}/contacts/search?q={email_id}"
            source_headers = {
            'api_access_token': source_token
            }
            response = requests.get(urlget, headers=source_headers)
            data = response.json()
            count = data["meta"]
            if count['count']!=None:
                if count['count']>0:
                            continue
                else:
                    
                    if (i.mobile_no or i.phone) and i.email_id:
                        mobile_no=''
                        phone=''
                        if i.mobile_no:
                            if len(i.mobile_no)==10:
                                mobile_no="+91"+str(i.mobile_no)
                            if len(i.mobile_no)==12:
                                mobile_no='+'+str(i.mobile_no)
                            if len(i.mobile_no)==13:
                                mobile_no=str(i.mobile_no)
                        else:
                            if len(i.phone)==10:
                                phone="+91"+str(i.phone)
                            if len(i.phone)==12:
                                phone='+'+str(i.phone)
                            if len(i.phone)==13:
                                phone=str(i.phone)

                        payload = {
                        'inbox_id': inbox_id,
                        'name': i.name,
                        'email': email_id,
                        'phone_number': mobile_no if mobile_no else phone,
                        }

                        headers = {
                        'api_access_token': source_token
                        }
                        files=[
                            
                        ]
                        response = requests.request("POST", url, headers=headers, data=payload, files=files)
                        if response.status_code==200:
                            countcon+=1
                        # frappe.msgprint(response.text)
        if countcon==0:
            frappe.msgprint("Contacts Already Synced !")
        else:
            frappe.msgprint(str(countcon)+" CRM Contacts Posted to OneHash Chat !")


    @frappe.whitelist()
    def fetch_contacts_from_chat(): 
        source_url = f"{base_url}/api/v1/accounts/{account_id}/contacts"
        source_headers = {
        'api_access_token': source_token
        }
        response = requests.get(source_url, headers=source_headers)

        if response.status_code == 200:
            data = response.json()
            contacts = data["payload"]
            
            for contact in contacts:
                
                full_name = contact["name"]
                lead_email = contact["email"]
                email_id = contact["email"]
                phone = contact["phone_number"]
                mobile_no = contact["phone_number"]
                city = contact["additional_attributes"].get("city", "")
                country = contact["additional_attributes"].get("country", "")
                product = "OneHash Chat"
                company_name = contact["additional_attributes"].get("company_name", "")
                status = "Open"
                
                get_contacts=frappe.db.get_all('Contact',fields=['*'],filters={'email_id':email_id,'phone':phone})
                get_contacts_ph=frappe.db.get_all('Contact',fields=['*'],filters={'phone':phone})
                if len(get_contacts)==0:
                    if not get_contacts and not get_contacts_ph:
                            l = frappe.get_doc(doctype='Lead', 
                            lead_name=full_name,
                            lead_email=lead_email,
                            email_id=email_id,
                            phone=phone,
                            mobile_no=mobile_no,
                            city=city,
                            country=country,
                            product=product,
                            company_name=company_name,
                            status=status)
                            l.insert()

    @frappe.whitelist()
    def fetch_user_account():
        source_url = f"{base_url}/api/v1/profile"
        source_headers = {
        'api_access_token': source_token
        }
        response = requests.get(source_url, headers=source_headers)
        
        if response.status_code == 200:
            data = response.json()
            fullname=str(data['available_name'])
            email=str(data['email'])
            role=str(data['role'])
            ocs.full_name=fullname
            ocs.email=email
            ocs.role=role
            ocs.save()
            frappe.msgprint('Profile Updaated')
        else:
            ocs.full_name=''
            ocs.email=''
            ocs.role=''
            ocs.save()

