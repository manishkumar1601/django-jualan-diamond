from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from tripay import Tripay
import tripay
from . import models, forms
import json, requests as r, base64
from telebot import TeleBot

tripay = Tripay()

def error_not_found(request, exception):
    return render(request, 'main/404.html')

def index(request):
    items = models.Item.objects.all()
    payments = models.Payment.objects.all()
    context = {
        "items": items,
        "payments":payments
    }
    return render(request, 'main/index.html', context)


def checkPurchase(request):
    if not request.GET.get("purchase_id"):
        return render(request, 'main/check-purchase.html')    

    payment_id = request.GET.get("purchase_id").replace("INV", "")
    if payment_id.isdigit():
        payment_id = int(payment_id)
    else:
        return render(request, 'main/check-purchase.html')    
    
    order = models.Order.objects.filter(id = payment_id).first()
    return render(request, 'main/check-purchase.html' , {"order":order, "keren":True})    


@csrf_exempt
def checkId(request):
    res = {}
    request.GET.update(request.POST)
    form = forms.CheckIdForm(request.GET)
    if form.is_valid():
        res["status"] = True
        url = "https://www.smile.one/merchant/mobilelegends/checkrole/"
        headers = {'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'content-length': '62', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'origin': 'https://www.smile.one', 'referer': 'https://www.smile.one/merchant/mobilelegends?source=other', 'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"', 'sec-ch-ua-mobile': '?0', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'x-requested-with': 'XMLHttpRequest'}
        payload = {}
        payload["user_id"] = request.GET["id"]
        payload["zone_id"] = request.GET["server"]
        payload["pid"] = 26
        payload["checkrole"] = 1

        msg = base64.b64encode(r.post(url, headers = headers, data = payload).content).decode()
        error_msg = base64.b64encode(r.post(url, headers = headers, data = {"user_id":"123456789", "zone_id":"1234", "pid":26, "checkrole":1}).content).decode()
        if msg == error_msg:
            res["is_valid"] = False
        else:
            res["is_valid"] = True

        return HttpResponse(json.dumps(res))
    else:
        res["status"] = False
        res["is_valid"] = None
        return HttpResponse(json.dumps(res), status = 400)

@require_POST
def generatePayment(request):
    res = {}
    form = forms.GeneratePaymentForm(request.POST)

    if form.is_valid():

        try:
            item = models.Item.objects.get(id = form.cleaned_data["item"])
        except:
            return HttpResponse("KONTOLODON", status = 400)

        try:
            payment = models.Payment.objects.get(code_name = form.cleaned_data["payment"])
        except:
            return HttpResponse("KONTOLODON", status = 400)

        order = models.Order(
            userid = form.cleaned_data["userid"],
            zoneid = form.cleaned_data["zoneid"],
            item = item,
            nowa = form.cleaned_data["nowa"],
            pay_with = payment
        )
        order.save()

        result = tripay.create_payment(item.price_in_idr, "INV" + str(order.id), item, method = payment.code_name)
        del result["data"]["callback_url"]
        return HttpResponse(json.dumps(result))

    return HttpResponse("OK")