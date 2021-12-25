from sellerSide import models as sell_models
from django.shortcuts import render, redirect
from . import models as sec_user_models
import string
import random
from datetime import datetime
from django.db.models import Q
from midtransclient import Snap, CoreApi
import json
import requests as rq

SERVER_KEY = 'Mid-server-i1A9vgpsxiWD71rhc_M3EZya'
CLIENT_KEY = 'Mid-client-J6Nn40pIMpSE7apJ'


def view_cart(request, state = 'cart'):
	obj_carts = sell_models.cart.objects.filter(buyer = request.user, state_order = state)
	all_prd = []
	for x in range(len(obj_carts)):
		all_prd.append(obj_carts[x].stuff)

	items = {i:all_prd.count(i) for i in all_prd}
	keys_item = list(items.keys())
	value_item = list(items.values())

	arr_view = []
	for x in range(len(keys_item)):
		obj_post = sell_models.products_post.objects.get(stuff_fk = keys_item[x])
		img_file = keys_item[x].img_file.split(('^!@!^'))
		arr_view.append([keys_item[x], obj_post, img_file ,value_item[x]])
	# print(arr_view)
	return arr_view

# def get_user(request):
# 	obj_user_sec = sec_user_models.user_sec.objects.get(fk_id_user = request.user)

# Hanya untuk menset tampilan datanya tanpa disave
def set_for_pay(request, stuff_data):
	obj_user_sec = sec_user_models.user_sec.objects.get(fk_id_user = request.user)
	address = obj_user_sec.address
	phone_num = obj_user_sec.phone
	price_stufs = 0
	price_ship = 0
	total = 0
	# data passing array
	for x in range(len(stuff_data)):
		pointer = False
		price_stufs += (stuff_data[x][0].price * stuff_data[x][3])
		if x == 0:
			if stuff_data[x][0].stuff_promo.promo_type.name == 'gratis_ongkir':
				price_ship += stuff_data[x][1].ship_cost*(stuff_data[x][0].stuff_promo.value/100)
			else:
				price_ship += stuff_data[x][1].ship_cost
		else:
			for y in range(len(stuff_data)):
				if y != x:
					if stuff_data[x][0].seller == stuff_data[y][0].seller:
						pointer = True
			if pointer == False:
				if stuff_data[x][0].stuff_promo.promo_type.name == 'gratis_ongkir':
					price_ship += stuff_data[x][1].ship_cost*(stuff_data[x][0].stuff_promo.value/100)
				else:
					price_ship += stuff_data[x][1].ship_cost

	total = price_stufs+price_ship
	obj_cart = sell_models.cart.objects.filter(buyer = request.user, state_order = 'order')

	return [address, price_stufs, price_ship, total, obj_cart, phone_num]

def action_control(request):
	# Proses 1 => Ubah data cart menjadi ordered
	# Proses 2 => Edit data alamat pembeli
	# Proses 2 => simpan Total bayar / trx ke models trx (buat lagi)
	# Proses 3 => simpan semua cart dan ID trx yang ordered ke selling models
	ids_prd = request.POST.getlist('id_stuffs')
	ids_post = request.POST.getlist('post_stuffs')
	address_buyer = request.POST.get('address')
	phone_buyer = request.POST.get('phone')
	obj_carts = []
	N = 15
  
	# using random.choices()
	# generating random strings 
	# print(ids_prd)
	obj_prd = []
	for x in range(len(ids_prd)):
		obj_prd.append(sell_models.stuff.objects.get(id = int(ids_prd[x])))
	trx_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
	for x in range(len(obj_prd)):
		obj_carts += sell_models.cart.objects.filter(buyer = request.user, stuff = obj_prd[x], state_order = 'order')

	if request.method == "POST" and request.POST.get('buy') != None:
		# print(obj_carts)
		ship_cost = request.POST.get('price_ship')
		stuff_cost = request.POST.get('price_stuff')
		total = request.POST.get('total')
		print(ship_cost, stuff_cost, total)
		# ubha semua cart menjadi ordered
		for x in range(len(obj_carts)):
			obj_carts[x].state_order = 'ordered'
			obj_carts[x].save()
		# edit data alamat
		obj_user_sec = sec_user_models.user_sec.objects.get(fk_id_user = request.user)
		obj_user_sec.address = address_buyer
		obj_user_sec.phone = phone_buyer
		obj_user_sec.save()
		# Menyimpan data ke selling models
		for x in range(len(obj_carts)):
			add_sell = sell_models.selling(
				date = datetime.now().date(),
				pay_value = 0,
				count = 1,
				# ship cost kosonngkan untuk sementara
				ship_cost = 0,
				pay_method = 'transfer',
				trx_id = trx_ID,
				cart_ordered = obj_carts[x],
				buyer = request.user
				)
			add_sell.save()
		# Menyimpan data de models trx beserta data pembelian
		add_trx = sec_user_models.trx_data(
			date = datetime.now().date(),
			trx_code = trx_ID,
			buyer = request.user,
			ship_cost = int(float(ship_cost)),
			stuff_cost = int(float(stuff_cost)),
			total_price = int(float(total))
			)
		add_trx.save()

	if request.method == "POST" and request.POST.get('cancel') != None:
		for x in range(len(obj_carts)):
			obj_carts[x].state_order = 'cart'
			obj_carts[x].save()

def set_process_status(trx_code, pay_status, pay_total):
	if pay_status != '':
		if pay_status == 200 or pay_status == '200':
			print('Pembayaran sukses')
			# Dapatkan selling dengan trx id
			sells = sell_models.selling.objects.filter(trx_id = trx_code)
			for x in range(len(sells)):
				cart = sells[x].cart_ordered
				# Mrngubah status
				cart.state_order = 'process'
				cart.state_buy = 'buyed'
				cart.save()
				sells[x].pay_value = pay_total
				sells[x].save()

			add = sell_models.profit(
				date = datetime.now().date(),
				profit_sell = pay_total,

				# Fk
				sell_code = sells[0]
				)
			add.save()
		elif pay_status == 201 or pay_status == '201':
			print('Pembayaran pending')
			# Dapatkan selling dengan trx id
			sells = sell_models.selling.objects.filter(trx_id = trx_code)
			for x in range(len(sells)):
				cart = sells[x].cart_ordered
				# Mrngubah status
				cart.state_order = 'ordered'
				cart.state_buy = 'pending'
				cart.save()
				sells[x].pay_value = 0
				sells[x].save()

			add = sell_models.profit(
				date = datetime.now().date(),
				profit_sell = 0,

				# Fk
				sell_code = sells[0]
				)
			add.save()
		return redirect('/oAuth/o_auth_order_pay')

def view_unpay (request):
	obj_selling = sell_models.selling.objects.filter(buyer = request.user, pay_value = 0)
	
	all_trx = []
	for x in range(len(obj_selling)):
		all_trx.append(obj_selling[x].trx_id)

	items = {i:all_trx.count(i) for i in all_trx}
	trx_code = list(items.keys())
	count_trx = list(items.values())

	carts = []
	stuffs = []
	transaction_token = []
	for x in range(len(trx_code)):
		carts.append(sell_models.selling.objects.filter(trx_id = trx_code[x], buyer = request.user))
		tmp = []
		for y in range(len(carts[x])):
			tmp.append(carts[x][y].cart_ordered.stuff.id)
		prd_ids = {i:tmp.count(i) for i in tmp}
		ids = list(prd_ids.keys())
		count_ids = list(prd_ids.values())
		tmp = []
		print(ids)
		for y in range(len(ids)):
			# print(ids[0])
			try:
				obj_prd = sell_models.stuff.objects.get(id = ids[y], state = 'active')
				obj_post = sell_models.products_post.objects.get(stuff_fk = obj_prd)
				tmp.append([obj_prd, obj_post, obj_prd.img_file.split('^!@!^')[0], count_ids[y]])
			except Exception as e:
				print(e)
		# Note : 1 tmp berisi banyak barang dalam 1 trx

		# Membuat checkout
		snap = Snap(
			is_production = True,
			server_key = SERVER_KEY,
			client_key = CLIENT_KEY,
			)

		# stuff_order = ctrl.view_cart(request, state = 'ordered')
		# print(stuff_order)
		# stuffs, trx = ctrl.view_unpay(request)
		# Buat checkout secara array
		# for x in range(trx):
		# id_trx = trx_code[x]
		amount = sec_user_models.trx_data.objects.get(trx_code = trx_code[x]).total_price
		snp = []
		pay_status = ''
		va_num = ''
		try:
			# token = snap.create_transaction_token({
			# 		"transaction_details":{
			# 			"order_id":trx_code[x],
			# 			"gross_amount":amount
			# 		}, "credit_card":{
			# 			"secure":True
			# 		}
			# 	})
			token = snap.create_transaction_token({
					"transaction_details":{
						"order_id":trx_code[x],
						"gross_amount":amount
					}, "credit_card":{
						"secure":True
					}
				})
			snp = token
			transaction_token.append(token)
		except Exception as e:
			# Mencari status dari checkout yang sudah pernaj dibuat
			url = 'https://api.midtrans.com/v2/'+trx_code[x]+'/status'

			payload = "\n\n"
			headers = {
			  'Accept': 'application/json',
			  'Content-Type': 'application/json',
			  'Authorization': 'Basic TWlkLXNlcnZlci1pMUE5dmdwc3hpV0Q3MXJoY19NM0VaeWE6'
			}

			response = rq.request("GET", url, headers=headers, data = payload)
			if response.status_code == 200 or response.status_code == '200':
				pay_status = json.loads(json.dumps(response.json()))['status_code']
				va_num = json.loads(json.dumps(response.json()))['va_numbers'][0]

			print(response.status_code)
			# print('\n',response.text.encode('utf8'),'\n')
			print(e)

		if pay_status != '':
			set_process_status(trx_code[x], pay_status, amount)

		stuffs.append([trx_code[x],tmp, snp, snap.api_config.client_key, pay_status, va_num])
		

	print(stuffs, trx_code)
	return stuffs, trx_code

def view_finish (request):
	obj_selling = sell_models.selling.objects.filter(Q(buyer = request.user) & ~Q(pay_value = 0))
	
	all_trx = []
	for x in range(len(obj_selling)):
		all_trx.append(obj_selling[x].trx_id)

	items = {i:all_trx.count(i) for i in all_trx}
	trx_code = list(items.keys())
	count_trx = list(items.values())

	sells = []
	stuffs = []
	stuffs_f = []
	stuffs_p = []
	for x in range(len(trx_code)):
		# state_order.append(sell_models.selling.objects.filter(trx_id = trx_code[x])[0].cart_ordered.state_order)
		sells.append(sell_models.selling.objects.filter(trx_id = trx_code[x], buyer = request.user))
		tmp = []
		for y in range(len(sells[x])):
			tmp.append(sells[x][y].cart_ordered.stuff.id)
			# state_order.append(sells[x][y].cart_ordered.state_order)
		prd_ids = {i:tmp.count(i) for i in tmp}
		ids = list(prd_ids.keys())
		count_ids = list(prd_ids.values())

		# Looping menentukan status order
		states_order = []
		for y in range(len(ids)):
			state_order = ''
			for z in range(len(sells[x])):
				if str(ids[y]) == str(sells[x][z].cart_ordered.stuff.id):
					state_order =  sells[x][z].cart_ordered.state_order
			# print(state_order, trx_code[x])
			states_order.append(state_order)

		tmp = []
		tmp1 = []
		tmp2 = []
		# print(ids)
		for y in range(len(ids)):
			# print(ids[0])
			obj_prd = sell_models.stuff.objects.get(id = ids[y])
			obj_post = sell_models.products_post.objects.get(stuff_fk = obj_prd)

			# sell_models.selling.objects.filter(trx_id = trx_code[x])[0].cart_ordered.state_order

			tmp.append([obj_prd, obj_post, obj_prd.img_file.split('^!@!^')[0], count_ids[y], states_order[y]])
			if states_order[y] == 'finish':
				tmp1.append([obj_prd, obj_post, obj_prd.img_file.split('^!@!^')[0], count_ids[y], states_order[y]])
			elif states_order[y] == 'process':
				tmp2.append([obj_prd, obj_post, obj_prd.img_file.split('^!@!^')[0], count_ids[y], states_order[y]])
		# Note : 1 tmp berisi banyak barang dalam 1 trx
		stuffs.append([trx_code[x],tmp])
		stuffs_f.append([trx_code[x],tmp1])
		stuffs_p.append([trx_code[x],tmp2])

	print(stuffs_f)
	return stuffs, trx_code, stuffs_p, stuffs_f

	# arr_view = []
	# for x in range(len(keys_item)):
	# 	obj_post = sell_models.products_post.objects.get(stuff_fk = keys_item[x])
	# 	img_file = keys_item[x].img_file.split(('^!@!^'))
	# 	arr_view.append([keys_item[x], obj_post, img_file ,value_item[x]])


def rating_system (request):
	if request.method == "POST":
		val = request.POST.get('review')
		id_prd = request.POST.get('id_prd')
		obj_prd = sell_models.stuff.objects.get(id = id_prd)
		add = sell_models.rating_data(
			value = val,
			stuff = obj_prd
			)
		add.save()

		sum_val = 0
		rates = sell_models.rating_data.objects.filter(stuff = obj_prd)
		for x in range(len(rates)):
			sum_val += rates[x].value
		sum_val = round(sum_val/len(rates))

		obj_prd.quality = sum_val
		obj_prd.save()

def finish_confirm (request):
	trx_id = request.POST.get('trx_ID')
	prd_id = request.POST.get('id_prd')

	obj_sells = sell_models.selling.objects.filter(trx_id = trx_id, buyer = request.user)
	for x in range(len(obj_sells)):
		print('sudah dicpba ubah', obj_sells[x].cart_ordered.stuff.id, prd_id)
		if str(obj_sells[x].cart_ordered.stuff.id) == str(prd_id):
			id_cart = obj_sells[x].cart_ordered.id
			obj_cart = sell_models.cart.objects.get(id = id_cart)
			obj_cart.state_order = 'finish'
			obj_cart.save()
			print('sudah dicpba ubah')

def view_post (request):
	obj_stuff = sell_models.stuff.objects.filter(seller = request.user, state = 'active')
	obj_posts = []
	for x in range(len(obj_stuff)):
		# print(obj_stuff[x])
		post = sell_models.products_post.objects.get(stuff_fk = obj_stuff[x].id)
		obj_posts.append([obj_stuff[x], post, obj_stuff[x].img_file.split('^!@!^')])

	return obj_posts


