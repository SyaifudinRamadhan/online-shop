from sellerSide import models as sell_models
from loginSys import models as user_models
from adminSide import models as admin_models
from django.db.models import Q
import operator
from datetime import datetime

def now_promos(view_for = 'example'):
	# Cari prouducts dengan promo tidak kosong berdasar urutan tanggal terbaru
	obj_promo = sell_models.promo.objects.filter(active = 'True').order_by('-start_date')
	
	key_promo = []

	if view_for == 'example':
		if len(obj_promo) >= 10:
			for x in range(10):
				key_promo.append(obj_promo[x])
		else:
			key_promo = obj_promo
	elif view_for == 'all_view':
		key_promo = obj_promo

	stuff_list = []
	for x in range(len(key_promo)):
		stuff_list += sell_models.stuff.objects.filter(stuff_promo = key_promo[x], state = 'active')

	data_all = []
	for x in range(len(stuff_list)):
		try:
			data_all.append(sell_models.products_post.objects.get(stuff_fk = stuff_list[x]))
		except Exception as e:
			print(e)

	# print(key_promo, stuff_list, data_all)
	# print(data_all[0].stuff_fk.price)
	data_all_arr = []
	for x in range(len(data_all)):
		img_file = data_all[x].stuff_fk.img_file.split('^!@!^')
		tmp =[data_all[x].stuff_fk.id, data_all[x].id, data_all[x].stuff_fk.name, data_all[x].stuff_fk.price, img_file, range(data_all[x].stuff_fk.quality)]
		data_all_arr.append(tmp)

	# print(data_all_arr[x])
	return data_all, data_all_arr

def fav_product(view_for = 'example'):
	# Dapatkan semua data penjualan
	obj = sell_models.selling.objects.all()

	all_selling = []
	for x in range(len(obj)):
		all_selling.append(obj[x].cart_ordered.stuff.id)
	# all_selling = [3,6,8,0,3,3,4,6,1,0,7,5,3,4,6,4,3,3]
	# print(all_selling)
	same_item = {i:all_selling.count(i) for i in all_selling}
	
	obj_id_prd = []
	for x in range(len(same_item)):
		max_val = max(same_item, key=same_item.get)
		obj_id_prd.append(max_val)
		del same_item[max_val
		]

	fav_id_prd = []

	if view_for == 'example':
		if len(obj_id_prd) >= 10:
			for x in range(10):
				fav_id_prd.append(obj_id_prd[x])
		else:
			fav_id_prd = obj_id_prd
	elif view_for == 'all_view':
		fav_id_prd = obj_id_prd

	fav_all = []
	for x in range(len(fav_id_prd)):
		try:
			if sell_models.stuff.objects.get(id = fav_id_prd[x]).state == 'active':
				fav_all.append(sell_models.products_post.objects.get(stuff_fk = fav_id_prd[x]))
		except Exception as e:
			print(e)

	# print(key_promo, stuff_list, data_all)
	# print(data_all[0].stuff_fk.price)
	fav_all_arr = []
	for x in range(len(fav_all)):
		img_file = fav_all[x].stuff_fk.img_file.split('^!@!^')
		tmp =[fav_all[x].stuff_fk.id, fav_all[x].id, fav_all[x].stuff_fk.name, fav_all[x].stuff_fk.price, img_file, range(0,fav_all[x].stuff_fk.quality)]
		fav_all_arr.append(tmp)

	# print(fav_all, fav_all_arr)
	return fav_all, fav_all_arr

def view_detail(request):
	data = []

	try:
		obj_post = sell_models.products_post.objects.get(id = request.GET.get('post'))
		obj_prd = sell_models.stuff.objects.get(id = request.GET.get('prd'))

		img = []

		tmp = obj_prd.img_file.split('^!@!^')
		for x in range(len(tmp)):
			if tmp[x] != '':
				if len(img) == 0:
					img.append([tmp[x], 'active'])
				else:
					img.append([tmp[x],''])
		obj_user_sec = user_models.user_sec.objects.get(fk_id_user = obj_prd.seller)
		data = [obj_prd.id, obj_post.id, obj_prd.name, obj_prd.price, obj_prd.count, obj_prd.desc, img,
		obj_prd.state, obj_post.note, obj_prd.seller.username, obj_user_sec.Photo, obj_prd.stuff_promo, range(0,obj_prd.quality)]
		print(data)
	except Exception as e:
		print(e)

	return data

def search_system(request):

	obj_src = []
	keyword = ''
	type_key = ''

	if request.method == "POST" and request.POST.get('Search') != None:
		obj_src = sell_models.stuff.objects.filter(Q(name__contains = request.POST.get('Search')) & Q(state = 'active'))
		keyword = request.POST.get('Search')
		type_key = 'general'

	# =========================== KOntrol filter seacrh =============================================

	elif request.method == "POST" and request.POST.get('flt') != None:
		word = request.POST.get('keyword')
		quality = request.POST.get('quality')
		if quality == None:
			quality = ''
		location = request.POST.get('location')
		if location == None:
			location = ''
		shipping = request.POST.get('shipping')
		if shipping == None:
			shipping = ''

		if request.POST.get('key_type') == 'general':
			# print("Cek search")
			# cari gratis ongkir
			keyword = word
			type_key = 'general'
			obj_promo_type = None
			try:
				obj_promo_type = admin_models.promo_type.objects.get(name = shipping)
			except Exception as e:
				print(e)
			obj_ship = []
			if obj_promo_type != None:
				obj_ship = sell_models.promo.objects.filter(promo_type = obj_promo_type)

			if len(obj_ship) == 0:
				obj_src = sell_models.stuff.objects.filter(
					Q(name__contains = word) & Q(quality__contains = quality) &
					Q(location__contains = location) & Q(state = 'active'))
			else:
				for x in range(len(obj_ship)):
					obj_src += sell_models.stuff.objects.filter(
						Q(name__contains = word) & Q(quality__contains = quality) &
						Q(location__contains = location) & Q(stuff_promo = obj_ship[x]) & Q(state = 'active'))
			# print(word, pay, min_price, max_price, quality, location, shipping)
		elif request.POST.get('key_type') == 'category':
			keyword = word
			type_key = 'category'
			cat_list = admin_models.category.objects.filter(Q(name__contains = word))

			obj_promo_type = None
			try:
				obj_promo_type = admin_models.promo_type.objects.get(name = shipping)
			except Exception as e:
				print(e)
			obj_ship = []
			if obj_promo_type != None:
				obj_ship = sell_models.promo.objects.filter(promo_type = obj_promo_type)

			if len(obj_ship) == 0:
				for x in range(len(cat_list)):
					obj_src += sell_models.stuff.objects.filter(Q(stuff_cat = cat_list[x]) & 
						Q(quality__contains = quality) &
						Q(location__contains = location) & Q(state = 'active'))
			else:
				for x in range(len(obj_ship)):
					for y in range(len(cat_list)):
						obj_src += sell_models.stuff.objects.filter(Q(stuff_cat = cat_list[y]) & 
							Q(quality__contains = quality) &
							Q(location__contains = location) & Q(stuff_promo = obj_ship[x]) & Q(state = 'active'))
					
		elif request.POST.get('key_type') == 'promo':
			# Cara mengembilnya sama dengan catagory namun ditambahi hanya 
			# yang memiliki promo
			keyword = word
			type_key = 'promo'
			cat_list = admin_models.category.objects.filter(Q(name__contains = word))

			obj_promo_type = None
			try:
				obj_promo_type = admin_models.promo_type.objects.get(name = shipping)
			except Exception as e:
				print(e)
			obj_ship = []
			if obj_promo_type != None:
				obj_ship = sell_models.promo.objects.filter(promo_type = obj_promo_type)

			if len(obj_ship) == 0:
				obj_all_promo = sell_models.promo.objects.all()
				for x in range(len(cat_list)):
					for y in range(len(obj_all_promo)):
						if obj_all_promo[y].promo_type.name != 'No Promo':
							obj_src += sell_models.stuff.objects.filter(Q(stuff_cat = cat_list[x]) & 
								Q(stuff_promo = obj_all_promo[y]) &
								Q(quality__contains = quality) &
								Q(location__contains = location) & Q(state = 'active'))
			else:
				for x in range(len(obj_ship)):
					for y in range(len(cat_list)):
						obj_src += sell_models.stuff.objects.filter(Q(stuff_cat = cat_list[y]) & 
							Q(quality__contains = quality) &
							Q(location__contains = location) & Q(stuff_promo = obj_ship[x]) & Q(state = 'active'))
					
	# ======================================================================================================================

	elif request.method == "GET" and request.GET.get('src') != None and request.GET.get('promo') != None:
		cat_list = admin_models.category.objects.filter(Q(name__contains = request.GET.get('src')))
		obj_all_promo = sell_models.promo.objects.all()

		for x in range(len(cat_list)):
			for y in range(len(obj_all_promo)):
				# print("Masuk cat promo", len(cat_list), len(obj_all_promo), obj_all_promo[y].promo_type.name)
				if obj_all_promo[y].promo_type.name != 'No Promo':
					obj_src += sell_models.stuff.objects.filter(stuff_cat = cat_list[x], stuff_promo = obj_all_promo[y], state = 'active')

		keyword  = request.GET.get('src')
		type_key = 'promo'

	elif request.method == "GET" and request.GET.get('src') != None:
		cat_list = admin_models.category.objects.filter(Q(name__contains = request.GET.get('src')))
		keyword = request.GET.get('src')
		type_key = 'category'
		for x in range(len(cat_list)):
			obj_src += sell_models.stuff.objects.filter(stuff_cat = cat_list[x], state = 'active')

	print(obj_src)

	post_prd = []
	for x in range(len(obj_src)):
		try:
			post_prd.append(sell_models.products_post.objects.get(stuff_fk = obj_src[x]))
		except Exception as e:
			print(e)

	# print(key_promo, stuff_list, data_all)
	# print(data_all[0].stuff_fk.price)
	src_all = []
	for x in range(len(post_prd)):
		img_file = post_prd[x].stuff_fk.img_file.split('^!@!^')
		tmp =[post_prd[x].stuff_fk.id, post_prd[x].id, post_prd[x].stuff_fk.name, post_prd[x].stuff_fk.price, img_file, range(0,post_prd[x].stuff_fk.quality)]
		src_all.append(tmp)

	return src_all, keyword, type_key

def add_cart(request, use_buy = False):
	print("masuk function")
	ID_stuff = ''
	if use_buy == False:
		if request.method == "POST":
			ID_stuff = request.POST.get('add_cart')
		elif request.method == "GET":
			ID_stuff = request.GET.get('add_cart')
	else:
		if request.method == "POST":
			ID_stuff = request.POST.get('check')
		elif request.method == "GET":
			ID_stuff = request.GET.get('check')
	obj_stuff = sell_models.stuff.objects.get(id = ID_stuff)
	state_buy = 'non'
	state_order = 'cart'
	date = datetime.now().date()

	add = sell_models.cart(
		stuff = obj_stuff,
		buyer = request.user,
		date = date,
		state_buy = state_buy,
		state_order = state_order,
		count = 1
		)

	add.save()

def min_cart(request, state = 'cart'):
	ID_stuff = ''
	if request.method == "POST":
		ID_stuff = request.POST.get('min_cart')
	elif request.method == "GET":
		ID_stuff = request.GET.get('min_cart')
	obj_stuff = sell_models.stuff.objects.get(id = ID_stuff)
	obj_cart = sell_models.cart.objects.filter(stuff = obj_stuff, state_order = state, buyer = request.user)
	obj_cart[0].delete()


def buy_system(request):
	data_IDs = request.POST.getlist('check')
	print(request.POST.getlist('check'))
	for x in range(len(data_IDs)):

		# if x != 0 and x != len(request.POST)-1:
		# Cek apakah ID produk suda masuk di cart
		obj_prd = sell_models.stuff.objects.get(id = data_IDs[x])
		check_prd = sell_models.cart.objects.filter(stuff = obj_prd, state_order = 'cart', buyer = request.user)
		if len(check_prd) == 0:
			# print("\nMasuk awal cart\n")
			add_cart(request, use_buy = True)
			obj_cart = sell_models.cart.objects.get(stuff = obj_prd, state_order = 'cart', buyer = request.user)
			obj_cart.state_order = 'order'
			obj_cart.save()
			
		else:
			for y in range(len(check_prd)):
				check_prd[y].state_order = 'order'
				check_prd[y].save()


def get_cart(request):
	pass