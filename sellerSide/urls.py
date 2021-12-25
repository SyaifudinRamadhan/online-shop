from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'home_seller'),
	path('my_product', views.product_mng, name = 'sell_product'),
	path('detail', views.product_detail, name = 'detail_product'),
	path('my_promo', views.promo_mng, name = 'sell_promo'),
	path('my_selling', views.selling_mng, name = 'sell_mng'),
	path('detail_sell', views.selling_detail, name = 'sell_detail'),
	path('my_saldo', views.saldo_mng, name = 'sell_saldo'),
]