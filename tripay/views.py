from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import Order
from config import TELEGRAM_BOT_TOKEN
from telebot import TeleBot
import json

bot = TeleBot(TELEGRAM_BOT_TOKEN)


def thank_you(request):
    order_id = request.GET.get("tripay_merchant_ref", "None")
    return render(request, "tripay/thank-you.html", {"order_id":order_id})


@csrf_exempt
def received_callback(request):
    data = json.loads(request.body.decode())

    payment_id = data["merchant_ref"].replace("INV", "")
    if payment_id.isdigit():
        payment_id = int(payment_id)

    order = Order.objects.get(id = payment_id)
    if data["status"] == "PAID":
        order.status = "SUDAH DIBAYAR"
        try:
            bot.send_message("862672392", f"Kamu dapat pesanan baru! #{order.id}")
            bot.send_message("1821585701", f"Kamu dapat pesanan baru! #{order.id}")
        except:
            passs
    elif data["status"] == "REFUND":
        order.status = "DIKEMBALIKAN"
    elif data["status"] == "EXPIRED":
        order.status = "KADALUARSA"
    
    order.save()
    return HttpResponse("!")