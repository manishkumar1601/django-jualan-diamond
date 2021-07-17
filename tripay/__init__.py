from config import TRIPAY_API_KEY, MERCHANT_CODE, TRIPAY_PRIVATE_KEY, HOST, SANDBOX
import requests as r
import hmac
import hashlib

class Tripay:
    def __init__(self):
        self.ses = r.Session()
        self.ses.headers.update({"Authorization":f"Bearer {TRIPAY_API_KEY}"})

    def create_signature(self, merchant_ref, amount):
        signStr = "{}{}{}".format(MERCHANT_CODE, merchant_ref, amount)
        signature = hmac.new(bytes(TRIPAY_PRIVATE_KEY,'latin-1'), bytes(signStr,'latin-1'), hashlib.sha256).hexdigest()
        return signature

    def create_payment(self, amount, merchant_ref, item, method = "QRIS", customer_name = "Anonymous", customer_email = "salismazaya@gmail.com",
                        ):
        json_data = {
            "method":method,
            "amount":amount,
            "merchant_ref":merchant_ref,
            "customer_name":customer_name,
            "customer_email":customer_email,
            "signature":self.create_signature(merchant_ref, amount),
            "callback_url":HOST + TRIPAY_PRIVATE_KEY + "/webhook",
            "return_url":HOST + "thank-you",
            "order_items": [{
                "sku":item.id,
                "name":item.name,
                "price":item.price_in_idr,
                "quantity":1
            }]
        }

        response = self.ses.post("https://tripay.co.id/api-sandbox/transaction/create" if SANDBOX else "https://tripay.co.id/api/transaction/create",
                json = json_data).json()

    
        if not response["success"]:
            raise Exception(response["message"])

        return response