from django.db import models
from django.contrib.auth.models import User


##################################
# STOCK #
##################################
class StockItem(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    add_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Stock(models.Model):
    UNITS = (
        ('KG', 'KG'),
        ('Grams', 'Grams'),
        ('Dozen', 'Dozen'),
        ('Liters', 'Liters'),
        ('Piece', 'Piece'),
        ('Plate', 'Plate'),
        ('Other', 'Other'),
    )

    STATUS = (
        ('Add', 'Add'),
        ('Remove', 'Remove'),
    )
    item = models.ForeignKey(StockItem, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(default=1.0)
    unit = models.CharField(max_length=20, default='KG', choices=UNITS)
    price = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, default='Add', choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True)
    add_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.item.name}-{self.quantity}'


##################################
# MENU #
##################################
class Category(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    add_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    UNITS = (
        ('KG', 'KG'),
        ('Grams', 'Grams'),
        ('Dozen', 'Dozen'),
        ('Liters', 'Liters'),
        ('Piece', 'Piece'),
        ('Plate', 'Plate'),
        ('Other', 'Other'),
    )

    STATUS = (
        ('Available', 'Available'),
        ('Out of Stock', 'Out of Stock'),
    )
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(default=1.0)
    unit = models.CharField(max_length=20, default='KG', choices=UNITS)
    price = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, default='Available', choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True)
    add_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    # class Meta:
    #     ordering = ['-date_created']

    def __str__(self):
        return f'{self.name}-{self.quantity}/{self.unit}'


##################################
# DEALS #
##################################
class Deal(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=1.0)
    date_created = models.DateTimeField(auto_now_add=True)
    add_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.name


class DealItem(models.Model):
    UNITS = (
        ('KG', 'KG'),
        ('Grams', 'Grams'),
        ('Dozen', 'Dozen'),
        ('Liters', 'Liters'),
        ('Piece', 'Piece'),
        ('Plate', 'Plate'),
        ('Other', 'Other'),
    )
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1.0)
    units = models.CharField(max_length=20, default='KG', choices=UNITS)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name + str(self.quantity)


##################################
# ORDER #
##################################
class Order(models.Model):
    STATUS = (
        ('Dine In', 'Dine In'),
        ('Takeaway', 'Takeaway'),
    )
    no = models.PositiveIntegerField(default=111, null=True, blank=True)
    order_taker_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, default='Dine In', choices=STATUS)
    charges = models.FloatField(default=1.0)
    bill = models.FloatField(default=1.0)
    discount = models.FloatField(default=0.0, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    add_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'Order# {self.id}'


class OrderItem(models.Model):
    item = models.ForeignKey(Deal, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(default=1.0)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.item.name}-{self.quantity}'


class OrderMenuItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(default=1.0)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.item.name}-{self.item.quantity}'
