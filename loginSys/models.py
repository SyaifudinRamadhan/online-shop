from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class user_sec (models.Model):
	fk_id_user = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.CharField(max_length = 10)
	Photo = models.CharField(max_length = 50, blank=True)
	address = models.TextField(blank=True)
	phone = models.CharField(max_length = 20, blank=True)

	def __str__(self):
		return str(self.fk_id_user)

class trx_data (models.Model):
	date = models.DateField()
	trx_code = models.CharField(max_length = 20)
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	ship_cost = models.IntegerField()
	stuff_cost = models.IntegerField()
	total_price = models.IntegerField()

	def __str__(self):
		return str(self.date)
