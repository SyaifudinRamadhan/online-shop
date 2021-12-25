from loginSys import models as login_data
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate as auth, login, logout
import os
from django.core.files.storage import FileSystemStorage
import base64 as enc
import json
import requests as rq
import random
import string

def login_core (request, dest = '/oAuth/', usr = '', passw = ''):
	username = usr
	pwd = passw
	if request.POST.get('login') != None :
		username = request.POST.get('username')
		pwd = request.POST.get('pwd')

	confirm = auth(request, username = username, password = pwd)

	if confirm != None :
		login(request, confirm)
		return dest
	else :
		return None

def login_check (request, dest_default = '/oAuth/', state = 'general'):
	if str(request.user) != 'AnonymousUser' :
		userSec = login_data.user_sec.objects.get(
			fk_id_user = User.objects.get(username = request.user).id
			)
		if state != userSec.status :
			if userSec.status == 'admin':
				return '/panel/'
			elif userSec.status == 'seller':
				return '/seller/'
			else :
				return dest_default
		else :
			return None

	else :
		return '/my_account'


def sign_up (request, dest = '/oAuth/'):
	username = request.POST.get('username')
	e_mail = request.POST.get('email')
	fname = request.POST.get('fname')
	lname = request.POST.get('lname')
	password = request.POST.get('pwd')

	create = User.objects.create_user(
		username = username, 
		password = password, 
		email = e_mail, 
		first_name = fname, 
		last_name = lname)
	create.save()
	# singup di user sec
	# keyUniq = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 25))
	user_sec = login_data.user_sec(
		fk_id_user = User.objects.get(username = username),
		status = 'general',
		Photo = 'default.jpg',
		)
	user_sec.save()

	# Auto login setelah sign up
	href = login_core(request, dest = dest, usr = username, passw = password)
	if href != None :
		return href
	else:
		return 'Login gagal, mungkin akun anda bermasalah'

def passConfirm (request, l_pass, new_pass, confirm):
	# ------------------- jadikan function ----------------------
	if l_pass != '' and new_pass != '' :
		authen = auth(request, username = request.user, password = l_pass)
		if authen != None :
			return True
		else :
			confirm.append('Konfirmasi password lama salah')
			print(confirm)
			return False
	elif (l_pass != '' and new_pass == '') or (l_pass == '' and new_pass != '') :
		confirm.append('Field password lama dan baru harus diisi')
		print(confirm)
		return False

def uploadImg (request, editSec, confirm) :
	# ------ Buat jadi function -----------
	fileState = False
	
	fileName = ''
	if len(request.FILES) != 0 :
		# Menghapus foto profil yang lama jika ada
		if editSec.Photo != '' and editSec.Photo != 'default.jpg':
			print(' g kosong')
			# Menghapus file lama
			# dirName = 'media/'+editSec.Photo
			try:
				# os.remove(dirName)
				url = "https://f-storage.000webhostapp.com/index.php?delete="+editSec.Photo
				response = rq.request('GET', url)
				print(response.json())
			except Exception as e:
				confirm.append('Gambar lama gagal dihapus')

		file = request.FILES['img']
		fileState = True
		print(request.method)
		print('\n', file.name)
		print('\n', len(request.FILES))

		# fs = FileSystemStorage()
		# file_upload = fs.save(file.name, file)

		# url = fs.url(file_upload)
		# fileName = url.split('/')
		data = {"file": enc.b64encode(file.open("rb").read())}
		url = "https://f-storage.000webhostapp.com/index.php?insert=true&type=png"
		response = rq.request('POST', url, data = data)
		if response.status_code == "200" or response.status_code == 200:
			jsonResponse = json.loads(json.dumps(response.json()))
			name = jsonResponse['filename']+"."+jsonResponse['type']
			print(response.json())
			fileName = name
			if name == "":
				fileName = "default.jpg"
		else:
			fileName = "default.jpg"
		# -----------------------------------------
		return fileState, fileName
	else :
		return fileState, fileName

def edit_acc(request):
	username = request.POST.get('username')
	e_mail = request.POST.get('email')
	fname = request.POST.get('fname')
	lname = request.POST.get('lname')
	password = request.POST.get('pwd')
	password2 = request.POST.get('pwd2')
	photo = request.FILES.get('img')

	confirm = []

	check = passConfirm(request, password, password2, confirm)

	obj = User.objects.get(username = request.user)

	obj.username = username
	obj.email = e_mail 
	obj.first_name = fname 
	obj.last_name = lname

	if password != '' and password2 != '':
		if check != False:
			obj.set_password(password2)

	obj_user_sec = login_data.user_sec.objects.get(fk_id_user = obj)

	status, file_name = uploadImg(request, obj_user_sec, confirm)
	if status == True:
		obj_user_sec.Photo = file_name

	try:
		obj.save()
		obj_user_sec.save()
	except Exception as e:
		print(e)
		confirm.append('Data gagal disimpan')

	if len(confirm) == 0:
		dest = login_core(request, usr = username, passw = password2)

	return confirm

