from . import models
from adminSide import models as admin_models
from loginSys import models as fk_user_main
from django.contrib.auth.models import User as user_main
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
import requests as rq
import base64 as enc
import json

# ---------------Reguler def functions -------------------------
def get_cat_list():
	category_list = []
	Cat = admin_models.category.objects.all()
	for x in range(len(Cat)):
		category_list.append([Cat[x].name, Cat[x].id])
	return category_list

def get_promo_list(request):
	t_promo_list = []
	t_promo = models.promo.objects.filter(seller = user_main.objects.get(username = request.user))
	for x in range(len(t_promo)):
			t_promo_list.append([t_promo[x].name, t_promo[x].id])
	return t_promo_list

def get_promo_cat_list():
	cat_promo_list = []
	Cat_promo = admin_models.promo_type.objects.all()
	for x in range(len(Cat_promo)):
		cat_promo_list.append([Cat_promo[x].name, Cat_promo[x].id])
	return cat_promo_list

def upload_img (request):
	file  = request.FILES.getlist('img')
	fs = FileSystemStorage()
	# Mengatasi upload multiple file
	file_name = ''
	for x in range(len(file)):
		# System upload pada local storage
		# upload = fs.save(file[x].name, file[x])
		# name = str(fs.url(upload)).split('/')
		# file_name += name[2] + '^!@!^'
		# System upload pada server storage
		
		data = {"file":enc.b64encode(file[x].open("rb").read())}
		# print(data)
		url = "https://f-storage.000webhostapp.com/index.php?insert=true&type=png"
		response = rq.request('POST', url, data = data)
		if response.status_code == 200 or response.status_code == '200':
			jsonResponse = json.loads(json.dumps(response.json()))
			print(jsonResponse['filename']+jsonResponse['type'])
			tmpName = jsonResponse['filename']+"."+jsonResponse['type']
			file_name += tmpName + '^!@!^'
		# print(file[x].open("rb").read())
		
	return file_name

def delete_img (request, class_model = models.stuff.objects):
	file_name = request.GET.get('del')
	# get nama file di db
	if request.GET.get('id') != None :
		id_stuff = request.GET.get('id')
		# object untuk digunakan edit data
		stuff_obj = class_model.get(id = id_stuff)
		getFileName = str(stuff_obj.img_file).split('^!@!^')
		new_file_name = ''
		for x in range(len(getFileName)):
			if str(getFileName[x]) != str(file_name) and str(getFileName[x]) != '':
				new_file_name += getFileName[x]+'^!@!^'
			elif str(getFileName[x]) == str(file_name):
				url = "https://f-storage.000webhostapp.com/index.php?delete="+getFileName[x]
				response = rq.request('GET', url)
				print(response.json())
				# try:
				# 	# dir_name = 'media/'+getFileName[x]
				# 	# os.remove(dir_name)

				# except Exception as e:
				# 	print(e,'\n')
		stuff_obj.img_file = new_file_name
		stuff_obj.save()
	else:
		print('Gagal menghapus. request tidak sesuai\n')

def get_photo_profile(fk_user):
	obj = fk_user_main.user_sec.objects.get(fk_id_user = fk_user)
	return obj.Photo

# ------------ untuk kontrol produk view page  dan view detail page -------
def view_product (request, id_data = 0):
	data_product = ''
	try:
		if id_data == 0:
			data_product = models.stuff.objects.filter(seller = request.user)
		else:
			data_product = models.stuff.objects.filter(seller = request.user, id = id_data)
	except Exception as e:
		print(e,'\n')
		return [], []

	listID = []
	listView = []

	for x in range(len(data_product)):
		obj_post = models.products_post.objects.get(stuff_fk = data_product[x])
		listID.append(data_product[x].id)
		ID = data_product[x].id
		name = data_product[x].name
		desc = data_product[x].desc
		img_dir = data_product[x].img_file.split('^!@!^')
		img_field = data_product[x].img_file
		state = data_product[x].state
		stock = data_product[x].count
		price = data_product[x].price
		location = data_product[x].location
		quality = data_product[x].quality
		# untuk mendapatkan category
		category = admin_models.category.objects.get(name = data_product[x].stuff_cat).name
		# unutk dapatkan promo
		promo = models.promo.objects.filter(name = data_product[x].stuff_promo)[0].name

		tmp = [ID, name, desc, img_dir, state, stock, price, category, promo, img_field, location, range(0,quality), obj_post.ship_cost, obj_post.note]

		# tmp = [ID, name, desc, img_dir, state, stock, price, category, promo, img_field, location, range(0,quality), obj_post.ship_cost, obj_post.note]

		listView.append(tmp)

	return listView, listID

def for_modal_choice (request):
	# Mendapatkan list option dari table FK untuk addStuff
	category_list = get_cat_list()
	t_promo_list = get_promo_list(request)

	return category_list, t_promo_list

def addStuff (request):
	if request.POST.get('add_stuff') != None:
		name = request.POST['name']
		state = request.POST['state']
		price = request.POST['price']
		stock = request.POST['stock']
		desc = request.POST['desc']
		loc = request.POST['location']
		stuff_cat = admin_models.category.objects.get(id = request.POST['cat'])
		stuff_promo = models.promo.objects.get(id = request.POST['promo'])
		seller = user_main.objects.get(username = request.POST['id_seller'])
		ship_cost = request.POST.get('ship_cost')
		note = request.POST.get('note')
		# File type
		img_dir = upload_img(request)

		if len(img_dir) > 255:
			img_dir = ''

		add = models.stuff(
			name = name,
			state = state,
			price = price,
			count = stock,
			desc = desc,
			img_file = img_dir,
			quality = 0,
			location = loc,
			stuff_cat = stuff_cat,
			stuff_promo = stuff_promo,
			seller = seller
			)
		add.save() 

		add_sec = models.products_post(
			date = datetime.now().date(),
			note = note,
			ship_cost = ship_cost,
			# FK
			stuff_fk = models.stuff.objects.get(name = name,
				state = state,
				price = price,
				count = stock,
				desc = desc,
				img_file = img_dir,
				quality = 0,
				location = loc,
				stuff_cat = stuff_cat,
				stuff_promo = stuff_promo,
				seller = seller)
			)
		add_sec.save()

	else:
		print('Tidak ada request add_stuff')

def editStuff (request):
	if request.POST.get('edit_stuff') != None:
		id_stuff = request.POST['id']
		name1 = request.POST['name']
		state1 = request.POST['state']
		price1 = request.POST['price']
		stock1 = request.POST['stock']
		desc1 = request.POST['desc']
		loc1 = request.POST['location']
		stuff_cat1 = admin_models.category.objects.get(id = request.POST['cat'])
		stuff_promo1 = models.promo.objects.get(id = request.POST['promo'])
		seller1 = user_main.objects.get(username = request.POST['id_seller'])

		stuff_obj = models.stuff.objects.get(seller = user_main.objects.get(username = request.user), id = id_stuff)
		
		# id_post = request.POST.get('id_sec')
		ship_cost = request.POST.get('ship_cost')
		note = request.POST.get('note')

		post_obj = models.products_post.objects.get(stuff_fk = stuff_obj)

		if len(request.FILES.getlist('img')) != 0 :
			print('Ono gambar e broo !!!\n')
			prev_img = stuff_obj.img_file
			img_dir = upload_img(request)

			img_dir = img_dir + prev_img

			if len(img_dir) > 255:
				img_dir = prev_img

			stuff_obj.name = name1
			stuff_obj.state = state1
			stuff_obj.price = price1
			stuff_obj.count = stock1
			stuff_obj.desc = desc1
			stuff_obj.img_file = img_dir
			stuff_obj.location = loc1
			stuff_obj.stuff_cat = stuff_cat1
			stuff_obj.stuff_promo = stuff_promo1
			stuff_obj.seller = seller1

			stuff_obj.save()

			post_obj.note = note
			post_obj.ship_cost = ship_cost

			post_obj.save()

		else:
			print('Gak ono gambar e broo !!!\n')
			stuff_obj.name = name1
			print(name1,'\n')
			stuff_obj.state = state1
			stuff_obj.price = price1
			stuff_obj.count = stock1
			stuff_obj.desc = desc1
			stuff_obj.location = loc1
			stuff_obj.stuff_cat = stuff_cat1
			stuff_obj.stuff_promo = stuff_promo1
			stuff_obj.seller = seller1

			stuff_obj.save()

			post_obj.note = note
			post_obj.ship_cost = ship_cost

			post_obj.save()

	else:
		print('Tidak ada request edit\n')

def del_stuff_data(request):
	confirm = True
	if request.GET.get('del_data') != None:
		del_data = ''
		try:
			del_data = models.stuff.objects.get(id = request.GET.get('del_data'))
			# del_data_sec = models.products_post.objects.get(stuff_fk = del_data)
		except Exception as e:
			print(e,'\n')
			confirm = False

		if confirm == True:
			# img = del_data.img_file
			# img = str(img).split('^!@!^')
			# for x in range(len(img)):
			# 	if img[x] != '':
			# 		try:
			# 			os.remove('media/'+img[x])
			# 		except Exception as e:
			# 			print(e,'\n')
			# del_data_sec.delete()
			# del_data.delete()
			del_data.state = 'deactive'
			del_data.save()
		return confirm

	else:
		print('Tidak ada request HAPUS\n')
		return confirm

# ------------------ KOntrol view promo dan edit promo ------------------
def view_promos(request, id_data = 0):
	data_promos = ''
	list_view = []
	if id_data == 0:
		data_promos = models.promo.objects.filter(seller = request.user)
	else :
		data_promos = models.promo.objects.filter(seller = request.user, id = id_data)

	for x in range(len(data_promos)):
		ID = data_promos[x].id
		name = data_promos[x].name
		start_prm = str(data_promos[x].start_date)
		end_prm = str(data_promos[x].end_date)
		desc = data_promos[x].desc
		val_prm = data_promos[x].value
		prm_type = data_promos[x].promo_type
		prm_icon = ''

		if prm_type.name == 'No Promo':
			prm_icon = 'img/no_promo.png'
		elif prm_type.name == 'gratis_ongkir':
			prm_icon = 'img/ongkir-gratis.png'
		elif prm_type.name == 'voucher_discount':
			prm_icon = 'img/voucher_dc.png'
		elif prm_type.name == 'voucher_cashback':
			prm_icon = 'img/cashback.png'
		# print(prm_type.name)
		tmp = [ID, name, start_prm, end_prm, desc, val_prm, prm_type, prm_icon]
		list_view.append(tmp)

	return list_view

def add_promo(request):
	if request.POST.get('add_promo') != None:
		name = request.POST.get('name')
		st_date = request.POST.get('st')
		end = request.POST.get('end')
		desc = request.POST.get('desc')
		val = request.POST.get('val')
		prm_type = admin_models.promo_type.objects.get(id = request.POST.get('tp_prm'))
		seller = user_main.objects.get(username = request.user)

		add = models.promo(
			name = name,
			start_date = st_date,
			end_date = end,
			desc = desc,
			value = val,
			promo_type = prm_type,
			seller = seller,
			)
		add.save()
	else:
		print('Tidak ada request POST add promo\n') 

def edit_promo(request):
	if request.POST.get('edit_promo') != None:
		ID = request.POST.get('id')
		name = request.POST.get('name')
		st_date = request.POST.get('st')
		end = request.POST.get('end')
		desc = request.POST.get('desc')
		val = request.POST.get('val')
		prm_type = admin_models.promo_type.objects.get(id = request.POST.get('tp_prm'))
		seller = user_main.objects.get(username = request.user)		

		edit = models.promo.objects.get(seller = user_main.objects.get(username = request.user), id = ID)

		edit.name = name
		edit.start_date = st_date
		edit.end_date = end
		edit.desc = desc
		edit.value = val
		edit.promo_type = prm_type
		edit.seller = seller

		edit.save()
	else:
		print('Tidak ada request EDIt data\n')

def del_promo_data(request):
	confirm = True
	if request.GET.get('del_data') != None:
		del_data = ''
		try:
			del_data = models.promo.objects.get(id = request.GET.get('del_data'))
		except Exception as e:
			print(e,'\n')
			confirm = False

		if confirm == True:
			del_data.delete()
		return confirm
	else:
		print('Tidak ada request HAPUS\n')
		return confirm


# -------------- Kontrol untuk selling barang oleh seller -------------
def view_selling(List_ID):
	list_view = []
	for x in range(len(List_ID)):
		# stuff_obj = models.stuff.objects.get(id = List_ID[x])
		obj = models.selling.objects.filter(name_stuff = models.stuff.objects.get(id = List_ID[x]))
		tmp = []
		for y in range(len(obj)):
			tmp.append(
					[str(obj[y].date), obj[y].pay_value, obj[y].count, obj[y].ship_cost,
					obj[y].pay_method, obj[y].buyer.username, obj[y].buyer, obj[y].id]
				)
		list_view.append(tmp)
	return list_view

# -------- Kontrol untuk get /view profit per tahun ------------
def create_view_all(ID_Stuff):
	all_saldo = []
	for x in range(len(ID_Stuff)):
		obj_sell = models.selling.objects.filter(
			name_stuff = models.stuff.objects.get(id = ID_Stuff[x]))
		for y in range(len(obj_sell)):
			obj_saldo = models.profit.objects.get(sell_code = obj_sell[y])
			all_saldo.append(obj_saldo)
	return all_saldo

def create_view_graph(list_sells):
	list_saldo = []
	for x in range(len(list_sells)):
		try:
			list_saldo.append(models.profit.objects.get(sell_code = list_sells[x][2]))
		except Exception as e:
			print(e)
	print(list_saldo)
	print(datetime.today().date())
	year_now = str(datetime.today().date()).split('-')[0]
	view = ['']*12
	month = ''
	for x in range(len(list_saldo)):
		date = str(list_saldo[x].date).split('-')

		if date[0] == year_now:
			# view.append(list_saldo[x])
			if x == 0:
				month = date[1]
				view[int(month)-1] = list_saldo[x].profit_sell
			elif x > 0 and date[1] == month:
				view[int(month)-1] += list_saldo[x].profit_sell
			elif x > 0 and date[1] != month:
				view[int(month)-1] = list_saldo[x].profit_sell
				month = date[1]
	print(view)
	return view

def selling_list(request):
	pass
	# ambil data semua barang yang ada di penjual
	stuffs = models.stuff.objects.filter(seller = request.user)
	# Ambil semua cart terkait barang itu
	carts = []
	for x in range(len(stuffs)):
		carts += models.cart.objects.filter(stuff = stuffs[x]).order_by('date')
	# Hubungan 1 to 1 dengan selling data
	# carts.order_by('id')
	carts.sort(reverse = True, key=lambda carts: carts.id)
	# print(carts)
	trxs = []
	sells_prd = []
	sells_finish = []
	for x in range(len(carts)):
		try:
			trxs.append(models.selling.objects.get(cart_ordered = carts[x]).trx_id)
		except Exception as e:
			print(e)
	
	# Dapatkan list trx beserta jumlah tip trx nya
	trxs_id = {i:trxs.count(i) for i in trxs}
	trx_ids = list(trxs_id.keys())
	count_trx_ids = list(trxs_id.values())
	# Ambil data selling setiap transaksi
	for x in range(len(trx_ids)):
		sells = models.selling.objects.filter(trx_id = trx_ids[x])
		# 1 sells punya 1 produk
		prd_in_sell = []
		for y in range(len(sells)):
			prd_in_sell.append(sells[y].cart_ordered.stuff.id)

		tmp_prd = {i:prd_in_sell.count(i) for i in prd_in_sell}
		prd_ids = list(tmp_prd.keys())
		count_prd_ids = list(tmp_prd.values())
		# print(prd_in_sell, trx_ids[x])
		# Looping menentukan status order
		states_order = []
		for y in range(len(prd_ids)):
			state_order = ''
			for z in range(len(sells)):
				if str(prd_ids[y]) == str(sells[z].cart_ordered.stuff.id):
					state_order =  sells[z].cart_ordered.state_order
			# print(state_order, trx_code[x])
			states_order.append(state_order)

		tmp_stuff = []
		tmp_finish = []
		for y in range(len(prd_ids)):
			obj_prd = models.stuff.objects.get(id = prd_ids[y])
			obj_post = models.products_post.objects.get(stuff_fk = obj_prd)
			tmp_stuff.append([obj_prd, obj_post, obj_prd.img_file.split('^!@!^')[0], count_prd_ids[y], states_order[y]])
			# print(tmp_stuff, x)
			if states_order[y] == 'finish':
				tmp_finish.append([obj_prd, obj_post, obj_prd.img_file.split('^!@!^')[0], count_prd_ids[y], states_order[y]])

		detail_buyer = fk_user_main.user_sec.objects.get(fk_id_user = sells[0].buyer)

		sells_prd.append([trx_ids[x], tmp_stuff, sells[0], detail_buyer])
		sells_finish.append([trx_ids[x], tmp_finish, sells[0], detail_buyer])

	# print(sells_prd)
	return sells_prd, trx_ids, sells_finish

	








