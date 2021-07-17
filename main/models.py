from django.db import models
from django.utils import timezone

class Item(models.Model):
    id = models.CharField(max_length = 10, primary_key = True)
    name = models.CharField(max_length = 100)
    price_in_idr = models.IntegerField()

    def __str__(self):
        return self.name
    

class Payment(models.Model):
    name = models.CharField(max_length = 20)
    code_name = models.CharField(max_length = 20, unique = True)
    image_url = models.URLField()

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        UNPAID = "BELUM DIBAYAR", "BELUM DIBAYAR"
        PAID = "SUDAH DIBAYAR", "SUDAH DIBAYAR"
        PROCCESS = "DIPROSES", "DIPROSES"
        RECEIVED = "DITERIMA", "DITERIMA"
        REFUND = "DIKEMBALIKAN", "DIKEMBALIKAN"
        EXPIRED = "KADALUARSA", "KADALUARSA"

    userid = models.IntegerField()
    zoneid = models.IntegerField()
    status = models.CharField(choices = Status.choices, default = Status.UNPAID, max_length = 20)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    pay_with = models.ForeignKey(Payment, on_delete = models.CASCADE)
    nowa = models.CharField(max_length = 20)
    time_order = models.DateTimeField(default = timezone.now) 


    def save(self, *args, **kwargs):
        try:
            data = self.__class__.objects.get(id = self.id)
            if data.status == "DITERIMA":
                pass
            else:
                super(self.__class__, self).save(*args, **kwargs)
        except:
            super(self.__class__, self).save(*args, **kwargs)

