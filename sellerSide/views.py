from django.shortcuts import render, redirect
from loginSys import general_fn as fn
from . import controller as ctrl
import json as simplejson
from django.contrib.auth.models import User
from loginSys import models as sec_user_models

# Create your views here.
def index (request):
	# Cek login status
	check = fn.login_check(request, state = 'seller')
	if check != None:
		return redirect(check)

	msg = ''

	obj_user = User.objects.get(username = request.user)
	obj_user_sec = sec_user_models.user_sec.objects.get(fk_id_user = obj_user)

	if request.method == "POST" and request.POST.get('edit') != None:
		msg = fn.edit_acc(request)
		if len(msg) == 0:
			return redirect('/oAuthSell')
	# print(len(msg))

	context = {

		'data':obj_user,
		'data_sec':obj_user_sec,
		'msg':msg,
		'len':len(msg),
	}

	return render(request,'seller_index.html', context)

def product_mng (request):
	# Cek login 
	check = fn.login_check(request, state = 'seller')
	if check != None:
		return redirect(check)

	view, ID = ctrl.view_product(request)
	category, promo = ctrl.for_modal_choice(request)
	access = 'yes'
	if len(category) == 0 or len(promo) == 0:
		access = 'no'

	if request.method == "POST":
		ctrl.addStuff(request)
		return redirect('/oAuthSell/my_product')

	if request.GET.get('del_data') != None:
		confirm = ctrl.del_stuff_data(request)
		if confirm == True:
			return redirect('/oAuthSell/my_product')

	context = {
		'data':view,
		'promo_choice':promo,
		'cat_choice':category,
		'access':access,
	}

	return render(request,'seller_product_mng.html', context)

def product_detail (request):
	# Cek login 
	check = fn.login_check(request, state = 'seller')
	if check != None:
		return redirect(check)

	if request.GET.get('id') == None or request.GET.get('id') == '':
		return redirect('/oAuthSell/my_product')

	view, ID = ctrl.view_product(request, id_data = request.GET.get('id'))
	category, promo = ctrl.for_modal_choice(request)

	if len(view) == 0:
		return redirect('/oAuthSell/my_product')

	access = 'yes'
	if len(category) == 0 or len(promo) == 0:
		access = 'no'

	if request.method == "POST":
		ctrl.editStuff(request)
		url = '/oAuthSell/detail?id='+str(request.GET.get('id'))
		return redirect(url)

	if request.GET.get('del') != None:
		ctrl.delete_img(request)
		url = '/oAuthSell/detail?id='+str(request.GET.get('id'))
		return redirect(url)

	context = {
		'data':view,
		'promo_choice':promo,
		'cat_choice':category,
		'access':access,
	}

	return render(request,'view_detail_product.html', context)

def promo_mng (request):
	# Cek login 
	check = fn.login_check(request, state = 'seller')
	if check != None:
		return redirect(check)

	view = ctrl.view_promos(request)
	cat_promo = ctrl.get_promo_cat_list()
	# print(view)
	access = 'yes'
	if len(cat_promo) == 0:
		access = 'no'

	if request.method == "POST" and request.POST.get('add_promo') != None:
		ctrl.add_promo(request)
		return redirect('/oAuthSell/my_promo')

	if request.method == "POST" and request.POST.get('edit_promo') != None:
		ctrl.edit_promo(request)
		return redirect('/oAuthSell/my_promo')

	if request.GET.get('del_data') != None:
		confirm = ctrl.del_promo_data(request)
		if confirm == True:
			return redirect('/oAuthSell/my_promo')

	context = {
		'data':view,
		'cat_promo':cat_promo,
		'access':access,
	}

	return render(request, 'seller_promo_mng.html',context)

def selling_mng(request):
	# Cek login
	check = fn.login_check(request, state = 'seller')
	if check != None:
		return redirect(check)

	selling, trx, finish = ctrl.selling_list(request)

	context = {
		'view':selling,
		'len_trx':len(trx),
	}

	return render(request, 'seller_sell_mng.html', context)

def selling_detail(request):
	# Cek login
	check = fn.login_check(request, state = 'seller')
	if check != None:
		return redirect(check)

	if request.GET.get('id') == None or request.GET.get('index') == None:
		return redirect('/oAuthSell/my_selling')

	if request.GET.get('id') == '' or request.GET.get('index') == '':
		return redirect('/oAuthSell/my_selling')

	view, ID = ctrl.view_product(request, id_data = request.GET.get('id'))
	sell_data = ctrl.view_selling(ID)
	sell_view = ''
	try:
		sell_view = sell_data[int(request.GET.get('index'))]
	except Exception as e:
		print(e)
		return redirect('/oAuthSell/my_selling')
	profile = []

	print(sell_view,sell_data)

	if len(sell_view) != 0:
		for x in range(len(sell_view)):
			sell_view[x].append(ctrl.get_photo_profile(sell_view[x][6]))

	context = {
		'data':view,
		'sell_view':sell_view,
		'profile':profile,
		'len_sell_data':len(sell_view)
	}

	return render(request, 'view_detail_selling.html', context)	

def saldo_mng(request):
	# Cek login
	check = fn.login_check(request, state = 'seller')
	if check != None:
		return redirect(check)

	selling, trx, finish = ctrl.selling_list(request)
	# view_all = []
	data_graph = ctrl.create_view_graph(finish)
	print(finish)

	context={
		'view':finish,
		'len_trx':len(trx),
		'graph_data':data_graph,
		}

	return render(request,'seller_saldo_mng.html',context)