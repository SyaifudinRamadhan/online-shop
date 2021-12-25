from django.urls import path
from . import views



urlpatterns = [
	path('', views.accLogged, name = 'account'),
	path('cart_oauth', views.cartLogged, name = 'cart'),
	path('o_auth_order', views.myaccOrder, name = 'order'),
	path('o_auth_order_pay', views.myaccOrder_pay, name = 'pay'),
	path('o_auth_order_process', views.myaccOrder_process, name = 'process'),
	path('o_auth_order_final', views.myaccOrder_final, name = 'finish'),
	path('flash_promo', views.flashPromo, name = 'flash_sell'),
	path('free_ongkir', views.promoOngkir, name = 'free_ongkir'),
	path('game_promo', views.gamePromo, name = 'game_promo'),
	path('vc_promo', views.vcoPromo, name = 'voucher_promo'),
	path('my_voucher', views.myAccVoucher, name = 'my_voucher'),
	path('reg_sell', views.regSeller, name = 'reg_seller'),
	path('post', views.post_view, name = 'post_view'),
	path('logout', views.log_out, name = 'logout'),
]