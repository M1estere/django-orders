# orders/models.py

from django.db import models
from typing import List, Any, Optional

class Item(models.Model):
    name: str = models.CharField(max_length=100)
    price: float = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    STATUS_CHOICES: List[tuple] = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number: int = models.IntegerField()
    items: models.ManyToManyField = models.ManyToManyField(Item, related_name='orders')
    total_price: float = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    status: str = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)
        self.update_total_price()

    def update_total_price(self) -> None:
        items = self.items.all()
        total = sum(item.price for item in items if item.price is not None)
        self.total_price = total
        Order.objects.filter(id=self.id).update(total_price=total)

    def __str__(self) -> str:
        return f"Заказ {self.id} - Стол #{self.table_number}"

    @classmethod
    def get_status_value(cls, display_name: str) -> Optional[str]:
        for value, name in cls.STATUS_CHOICES:
            if name.lower() == display_name.lower():
                return value
        return None
