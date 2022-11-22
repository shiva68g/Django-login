from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth import authenticate, login , logout
from .models import *
from .socialmedia import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail as sm





# user create backend 
def CreateUser(req):

	# generate otp
	otp = get_random_string(6, allowed_chars='0123456789')

	email = req.POST.get('email')
	name = req.POST.get('name')
	password = req.POST.get('password')
	confirmpassword = req.POST.get('confirmpassword')
	DOB = req.POST.get('DOB')
	name = req.POST.get('name')
	# validate the data 
	if(email == '' or name == '' or DOB == '' or password == ''):
		return render(req , 'register.html' , {'error' : True})

	# check the password and confirmpassword is same
	if(password == confirmpassword):

		# handle the user if he alredy exits
		try:
			user = MyUser.objects.create(
				email = email,
				name = name,
				date_of_birth = DOB,
				password = password
				)
			user.save()
			# after saveing the data send otp to email to veirify
			Otp = OtpCode(User=user , code = otp);
			Otp.save();
			sm(
				subject = 'VerifyOtp',
				message = 'Verify the Otp is ' + Otp.code, 
				from_email = 'fakedjango123@gmail.com',
				recipient_list = [user.email],
				fail_silently=False,
				)   
		 # if user alredy exits show  error in form 
		except Exception:
			
			return render(req , 'register.html' , {'error' : True})

		# login the user
		user = authenticate(req ,username=email, password=password)
		if user is not None:
			login(req ,user)
			return redirect('/otp')
		else:
			return render(req , 'register.html' , {'error' : True})

	# if password and confirmpassword are not same
	else:
		return render(req , 'register.html' , {'error' : True})




# user login backend validate data 
def UserLogin(req):

	# generate otp
	otp = get_random_string(6, allowed_chars='0123456789')


	email = req.POST.get('email')
	password = req.POST.get('password')
	if(email == '' or password == ''):
		return render(req , 'login.html' , {'error' : True})
	user = authenticate(req ,username=email, password=password)

	# check user is exits
	if user is not None:	
		login(req ,user)

		# if user exits then check if he is verified using otp 
		if(req.user.is_verified == False):

			# if user is not verified than verify him then redirect to home page
			Otp = OtpCode.objects.get(User=user);
			Otp.code = otp
			Otp.save();
			sm(
				subject = 'VerifyOtp',
				message = 'Verify the Otp is '+Otp.code,
				from_email = 'fakedjango123@gmail.com',
				recipient_list = [req.user.email],
				fail_silently=False,
				) 
			return redirect('/otp')
		else:

			# if user is verified than redirecte to home page
			return redirect('/')
	# if user is not exits
	else:
		return render(req , 'login.html' , {'error' : True})






# handleing get and post method
def register(req):
	#if method is post getting data using post menthod and saveing data
	if(req.method == "POST"): 
		return CreateUser(req)

	#if method is get than show register form
	elif(req.method == "GET"):
		return render(req , 'register.html')



def loginuser(req):

	#if method is post check user if he is registered
	if(req.method == 'POST'):
		return UserLogin(req)

	#if method is get than show the login form 
	elif(req.method == "GET"):
		return render(req , 'login.html')



def verifyotp(req):
	# if req method is post verify the otp which sent to email
	if(req.method == "POST"):
		otp = req.POST.get('otp')
		if(OtpCode.objects.filter(User=req.user , code=otp).exists()):
			req.user.is_verified = True
			req.user.save()
			return redirect('/')

	#if req method is get than show otp from
	elif(req.method == "GET"):
		return render(req , 'otp.html')



def home(req):
	# check if user is logged in
	if(req.user.is_authenticated):
		return render(req , 'home.html')
		
	# if user is not logged in redirect to login page
	else:
		return redirect('/login')



def userlogout(req):
	logout(req)
	return redirect('/login')