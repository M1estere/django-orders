# orders/models.py

from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField()
    items = models.ManyToManyField(Item, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_total_price()

    def update_total_price(self):
        items = self.items.all()
        total = sum(item.price for item in items if item.price is not None)
        self.total_price = total
        Order.objects.filter(id=self.id).update(total_price=total)


    def __str__(self):
        return f"Заказ {self.id} - Стол #{self.table_number}"

    @classmethod
    def get_status_value(cls, display_name):
        for value, name in cls.STATUS_CHOICES:
            if name.lower() == display_name.lower():
                return value
        return None
