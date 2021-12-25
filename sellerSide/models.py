from django.db import models
from django.contrib.auth.models import User
from adminSide import models as admin

# Create your models here.
# ------- dibawah ini bisa diatur seller dn admin -----------
class promo (models.Model):
	name = models.CharField(max_length = 50)
	start_date = models.DateField()
	end_date = models.DateField()
	desc = models.CharField(max_length = 100)
	value = models.FloatField()
	active = models.CharField(max_length = 10)
	# Fk
	promo_type = models.ForeignKey(admin.promo_type, on_delete = models.CASCADE)
	seller = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.name

class stuff (models.Model):
	name = models.CharField(max_length = 100)
	state = models.CharField(max_length = 10)
	price = models.IntegerField()
	count = models.IntegerField()
	desc = models.CharField(max_length = 100, blank = True)
	img_file = models.CharField(max_length = 255, blank = True)
	dummy = models.CharField(max_length =10, blank=True)
	quality = models.IntegerField()
	location = models.CharField(max_length = 100)

	# FK
	stuff_cat = models.ForeignKey(admin.category, on_delete = models.CASCADE)
	stuff_promo = models.ForeignKey(promo, on_delete = models.SET(''))
	seller = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.name

class cart (models.Model):
	# FK
	stuff = models.ForeignKey(stuff, on_delete = models.CASCADE)
	buyer = models.ForeignKey(User, on_delete = models.DO_NOTHING)
	
	date = models.DateField()
	# state buy non, buyed, => ketika sudah dibayar
	state_buy = models.CharField(max_length = 15)
	# state order non, cart, order, ordered, process, finish
	state_order = models.CharField(max_length = 15)
	count = models.IntegerField()
	comment = models.CharField(max_length = 255, blank = True)

	def __str__(self):
		return str(self.date)

class selling (models.Model):
	date = models.DateField()
	pay_value = models.IntegerField()
	count = models.IntegerField()
	ship_cost = models.IntegerField()
	pay_method = models.CharField(max_length = 50)
	trx_id = models.CharField(max_length = 20, blank = True)

	# FK
	# name_stuff = models.ForeignKey(stuff, on_delete = models.DO_NOTHING)
	cart_ordered = models.ForeignKey(cart, on_delete = models.DO_NOTHING)
	buyer = models.ForeignKey(User, on_delete = models.DO_NOTHING)

	# def __str__(self):
	# 	return str(self.date)

class profit (models.Model):
	date = models.DateField()
	profit_sell = models.IntegerField()

	# Fk
	sell_code = models.ForeignKey(selling, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.date)

class products_post(models.Model):
	date = models.DateField()
	note = models.TextField(max_length=255)
	ship_cost = models.IntegerField()
	# FK
	stuff_fk = models.ForeignKey(stuff, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.date)

class rating_data (models.Model):
	value = models.IntegerField()
	# FK
	stuff = models.ForeignKey(stuff, on_delete=models.CASCADE)
