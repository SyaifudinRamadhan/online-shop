from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate as auth, login, logout
from loginSys import general_fn as fn
from . import controller as ctrl

def home(request):
	from loginSys import views

	views.cek(request)

	data_now_promo, data_now_promo_2 = ctrl.now_promos(view_for = 'example')
	# print(data_now_promo_2)
	fav_item, fav_item_2 = ctrl.fav_product(view_for = 'example')
	# print(fav_item)

	context = {
		'view':data_now_promo_2,
		'view_fav':fav_item_2,
	}

	return render(request,'home.html', context)

def searchPage(request):

	data, keyword, key_type = ctrl.search_system(request)

	blank = 'yes'
	if len(data) != 0:
		blank = 'no'

	context = {
		'view':data,
		'blank':blank,
		'keyword':keyword,
		'key_type':key_type,
	}

	return render(request,'page_search.html', context)

def promoPage(request):

	data_now_promo, data_now_promo_2 = ctrl.now_promos(view_for = 'all_view')
	# print(data_now_promo_2)

	context = {
		'promos':data_now_promo_2,
	}

	return render(request,'promo_page.html', context)

def favPage(request):

	fav_item, fav_item_2 = ctrl.fav_product(view_for = 'all_view')
	# print(fav_item)

	context = {
		'view_fav':fav_item_2,
	}

	return render(request,'fav_page.html', context)

def myAccountPage(request):
	note = ''
	# Cek login
	confirm = fn.login_check(request)
	if confirm != '/my_account':
		return redirect('/oAuth/')

	if request.method == "POST":
		# Untuk sign Up
		if request.POST.get('singup') != None :
			href = fn.sign_up(request)
			if href != None :
				return redirect(href)
			else:
				note = 'Signup gagal, mungkin data anda bermasalah'

		elif request.POST.get('login') != None :
			# untuk login
			href = fn.login_core(request)
			if href != None :
				return redirect(href)
			else:
				note = 'Login gagal, mungkin akun anda bermasalah'

	context = {
		'confirm':note,
	}

	return render(request,'my_acc_page.html', context)

def myCart(request):
	# Cek login
	note = ''
	# Cek login
	confirm = fn.login_check(request)
	if confirm != '/my_account':
		return redirect('oAuth/cart_oauth')

	if request.method == "POST":
		# Untuk sign Up
		if request.POST.get('singup') != None :
			note = fn.sign_up(request, dest = '/oAuth/cart_oauth')

		elif request.POST.get('login') != None :
			# untuk login
			href = fn.login_core(request, dest = '/oAuth/cart_oauth')
			if href != None :
				return redirect(href)
			else:
				note = 'Login gagal, mungkin akun anda bermasalah'

	context = {
		'confirm':note,
	}

	return render(request, 'my_cart_page.html', context)

def details(request):

	data = []

	if request.method == "POST" and request.POST.get('cart') != None:
	# 	print("Memambah keranjang")
		confirm = fn.login_check(request)
		if confirm == '/my_account':
			print('belum login')
			return redirect('oAuth/cart_oauth')
		else:
			# print(confirm)
			url = '/detail?prd='+str(request.POST.get('add_cart'))+'&post='+str(request.POST.get('ID_Post'))
			ctrl.add_cart(request)
			return redirect(url)

	if request.method == "POST" and request.POST.get('buy') != None:
	# 	print("Memambah keranjang")
		confirm = fn.login_check(request)
		if confirm == '/my_account':
			print('belum login')
			return redirect('oAuth/cart_oauth')
		else:
			# print(confirm)
			url = '/detail?prd='+str(request.POST.get('check'))+'&post='+str(request.POST.get('ID_Post'))
			# print(request.POST.getlist('check'))
			ctrl.buy_system(request)
			return redirect('/oAuth/o_auth_order')

	if request.method == 'GET' and request.GET.get('post') != None and request.GET.get('prd') != None:
		data = ctrl.view_detail(request)

	if len(data) == 0:
		print(data)
		return redirect('/')

	img_nav = []

	for x in range(len(data[6])):
		tmp = [x, x+1]
		img_nav.append(tmp)

	context = {
		'view':data,
		'nav':img_nav,
	}

	return render(request,'details.html', context);