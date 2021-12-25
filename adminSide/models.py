from django.db import models

# Create your models here.
# --- dua class ini hanya akan bisa diatur oleh admin -----
class category (models.Model):
	name = models.CharField(max_length = 50)
	desc = models.CharField(max_length = 100)

	def __str__(self):
		return self.name

class promo_type (models.Model):
	# Malsudnya promo tipe adalah jenis promonya. Seperti promoongkir, diskon bulanan dll
	name = models.CharField(max_length = 20)
	field_discount = models.TextField(max_length = 1000)

	def __str__(self):
		return self.name
# ==========================================================

