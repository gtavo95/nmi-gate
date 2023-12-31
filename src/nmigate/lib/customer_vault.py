
from nmigate.util.wrappers import log, postProcessingOutput, postProcessXml
from nmigate.lib.nmi import Nmi
import requests
import uuid


class CustomerVault(Nmi):
    def __init__(self, token, org):
        super().__init__(token, org)

    @postProcessingOutput
    def create_customer_vault(self, vault_request):
        uid = uuid.uuid4().hex,

        data = {
            "customer_vault": "add_customer",
            "security_key": self.security_token,
            "customer_vault_id": vault_request['id'] if vault_request['id'] else uid,
            "payment_token": vault_request['token'],
            "billing_id": vault_request['billing_id']
        }
        data.update(vault_request['billing_info']) 
        response = requests.post(url="https://secure.nmi.com/api/transact.php", data=data)
        return {"response": response, "type": 'create_customer_vault'}

    @postProcessingOutput
    def validate_customer_vault(self, user_id:str):
        url = "https://secure.networkmerchants.com/api/transact.php"
        query = {
            "security_key": self.security_token,
            "customer_vault_id": user_id,
            "amount": "0.00",
            "type": "validate"
        }
        response = requests.post(url=url, data=query)        
        return {"response": response, "type": 'create_customer_vault'}



    @postProcessXml
    def get_billing_info_by_transaction_id(self, transaction_id):
        url = "https://secure.nmi.com/api/query.php"
        query = {
            "security_key": self.security_token,
            "transaction_id": transaction_id,
        }
        response = requests.post(url=url, data=query)        
        return response 


    @postProcessXml
    def get_customer_info(self, id):
        url = "https://secure.nmi.com/api/query.php"
        query = {
            "report_type": "customer_vault",
            "security_key": self.security_token,
            "customer_vault_id": id
        }
        response = requests.post(url=url, data=query)        
        return response