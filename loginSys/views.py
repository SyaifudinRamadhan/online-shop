from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models as sec_user_models
from . import general_fn as fn
from django.contrib.auth import logout
from django.contrib.auth.models import User
from . import controller as ctrl
from online_shop import controller as ctrl_sell
from sellerSide import models as sell_models
from midtransclient import Snap, CoreApi
import json

SERVER_KEY = 'Mid-server-i1A9vgpsxiWD71rhc_M3EZya'
CLIENT_KEY = 'Mid-client-J6Nn40pIMpSE7apJ'

# Create your views here.

def cek(request):
	print("hello")

def cartLogged (request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	if request.method == "GET" and request.GET.get('add_cart') != None:
		try:
			ctrl_sell.add_cart(request)
		except Exception as e:
			print(e)

	if request.method == "GET" and request.GET.get('min_cart') != None:
		try:
			ctrl_sell.min_cart(request)
		except Exception as e:
			print(e)

	if request.method == "POST" and request.POST.get('buy') != None:
		ctrl_sell.buy_system(request)
		return redirect('/oAuth/o_auth_order')

	view = ctrl.view_cart(request)

	context = {
		'view':view,
		'len_view':len(view),
	}

	return render(request, 'my_cart_logged.html', context)

def accLogged (request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	msg = ''

	obj_user = User.objects.get(username = request.user)
	obj_sec_user = sec_user_models.user_sec.objects.get(fk_id_user = obj_user)

	if request.method == "POST" and request.POST.get('edit') != None:
		msg = fn.edit_acc(request)
		if len(msg) == 0:
			return redirect('/oAuth/')
	# print(len(msg))

	context = {
		'data_sec':obj_sec_user,
		'data':obj_user,
		'msg':msg,
		'len':len(msg),
	}

	return render(request, 'my_acc_logged.html', context)

def myaccOrder(request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	if request.method == "GET" and request.GET.get('min_cart') != None:
		try:
			ctrl_sell.min_cart(request, state = 'order')
		except Exception as e:
			print(e)

	view = ctrl.view_cart(request, state = 'order')
	set_other = ctrl.set_for_pay(request, view)
	# print(set_other)

	if request.method == "POST" and request.POST.get('buy') != None:
		ctrl.action_control(request)
		return redirect('/oAuth/o_auth_order_pay')

	if request.method == "POST" and request.POST.get('cancel') != None:
		ctrl.action_control(request)
		return redirect('/oAuth/o_auth_order')

	
	context = {
		'view':view,
		'len_view':len(view),
		'other':set_other,
	}

	return render(request, 'my_acc_order/my_acc_order_confirm.html', context)

def myaccOrder_pay(request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	snap = Snap(
		is_production = True,
		server_key = SERVER_KEY,
		client_key = CLIENT_KEY,
		)

	transaction_token = []
	# stuff_order = ctrl.view_cart(request, state = 'ordered')
	# print(stuff_order)
	stuffs, trx = ctrl.view_unpay(request)
	# # Buat checkout secara array
	# for x in range(trx):
	# 	id_trx = trx[x]
	# 	amount = sec_user_models.user_sec.objects.get(trx_code = trx[x]).total_price

	# 	try:
	# 		token = snap.create_transaction_token({
	# 				"transaction_details":{
	# 					"order_id":order_id,
	# 					"gross_amount":amount
	# 				}, "credit_card":{
	# 					"secure":True
	# 				}
	# 			})
	# 		transaction_token.append(token)
	# 	except Exception as e:
	# 		print(e)

	print(snap.api_config.client_key)

	context = {
		'trx':trx,
		'view':stuffs,
		'len_trx':len(trx),
		# 'tokens':transaction_token,
		'client_key':snap.api_config.client_key,
	}

	return render(request, 'my_acc_order/my_acc_order_payment.html', context)

def myaccOrder_process(request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	if request.method == "POST" and request.POST.get('finish') != None:
		ctrl.finish_confirm(request)
		return redirect('/oAuth/o_auth_order_final')

	stuffs, trx, process, finish = ctrl.view_finish(request)
	# print(stuffs, trx, len(trx))

	context = {
		'trx':trx,
		'view':process,
		'len_trx':len(trx)
	}

	return render(request, 'my_acc_order/my_acc_order_process.html', context)

def myaccOrder_final(request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	if request.method == "POST" and request.POST.get('review') != None:
		ctrl.rating_system(request)
		return redirect('/oAuth/o_auth_order_final')

	stuffs, trx, process, finish = ctrl.view_finish(request)
	# print(stuffs, trx, len(trx))

	context = {
		'trx':trx,
		'view':finish,
		'len_trx':len(trx)
	}

	return render(request, 'my_acc_order/my_acc_order_final.html', context)


def flashPromo (request):

	print(request.user)

	context = {
		'judul':'Voucher Promo Flash',
		'count' : True,
		'data' : [0,0,0,0,0,0],
	}
	

	return render(request, 'super_shop_day/flash_promo.html', context)
	# return HttpResponse('Ini berisi logika sistem untuk memanggil halaman tertentu')

def promoOngkir (request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	print(request.user)

	context = {
		'judul':'Voucher Promo Flash',
		'count' : True,
		'data' : [0,0,0,0,0,0],
	}
	

	return render(request, 'super_shop_day/free_ongkir.html', context)

def gamePromo (request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	print(request.user)

	context = {
		'judul':'Voucher Promo Flash',
		'count' : True,
		'data' : [0,0,0,0,0,0],
	}
	

	return render(request, 'super_shop_day/game_promo.html', context)

def vcoPromo (request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	print(request.user)

	context = {
		'judul':'Voucher Promo Flash',
		'count' : True,
		'data' : [0,0,0,0,0,0],
	}
	

	return render(request, 'super_shop_day/voucher_promo.html', context)

def myAccVoucher (request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	return render(request, 'my_pocket/my_acc_voucher.html')

def regSeller (request):
	# Cek login general
	confirm  = fn.login_check(request)
	if confirm == '/my_account':
		return redirect(confirm)

	if request.method == "POST" and request.POST.get('as_seller') != None:
		regis = sec_user_models.user_sec.objects.get(fk_id_user = request.POST.get('id'))
		print('Set seller\n')
		if regis.status != 'seller':
			regis.status = 'seller'
			regis.save()
			print('seller di set\n')
			return redirect('/oAuth/post')
		else:
			return redirect('/oAuth/post')

	context = {
		'judul':'Mulai Jualan',
	}

	return render(request, 'start_sell/my_start_sell.html', context)

# Masih pengembangan (bagian ini hanya untuk menampilkan seluruh postingan)
def post_view (request):
	# Cek login untuk halaman khusus
	confirm  = fn.login_check(request, state = 'seller')
	print(confirm)
	if confirm != None and confirm != '/oAuth/':
		# print(confirm)
		return redirect(confirm)
	elif confirm == '/oAuth/':
		return render(request, 'my_acc_post/std_acc_post.html')
	else :
		# Mengambil data dari post product
		view = ctrl.view_post(request)
		print(view)
		context = {
			'view':view
		}
		return render(request, 'my_acc_post/my_acc_post.html', context)

def log_out (request):
	if request.user != 'AnonymousUser' :
		logout(request)
		return redirect('/')
	else :
		return redirect('/')
	return redirect('/')