from django.shortcuts import render
from django.contrib.auth.models import auth
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from tumcathcom import settings
from portal.models import User
from voting.models import mainOfficeCadidate, choirCadidate, sccCadidate, cmaCadidate, claCadidate, authenticateVoting
from home.models import contactUsMessage
from portal.forms import UserForm
from django.contrib.auth.decorators import login_required
import random
import string

from api.serializers import membersSerializer
import csv
from django.http import HttpResponse
#import reportlab
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
# Create your views here.
def login(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        check_email = User.objects.filter(email=email).exists()
        check_is_superuser = User.objects.filter(email=email, is_superuser=True).exists()
        user = authenticate(request, username=email, password=password,is_superuser=True)
        
        if email =="":
            return render(request, 'adminportal/login.html',{"msg1":"Fill the Email field"})

        if password =="":
            return render(request, 'adminportal/login.html',{"msg1":"Fill the password field"})

        if check_email == False:
            return render(request, 'adminportal/login.html',{"msg1":"The email does not exist in our database!"})

        if user is  None:
            return render(request, 'adminportal/login.html',{"msg1":"Invalid Password!"})

        if check_is_superuser == False:
            return render(request, 'adminportal/login.html',{"msg1":"You are not authorized to access this portal!"})

        else:
            auth.login(request, user)			
            request.session['semail'] = email  
            return redirect('admin-dashboard')
            
    else:
        return render(request, 'adminportal/login.html')
		
def password_reset(request, *args, **kwargs):
	if request.method == 'POST':
		email = request.POST['email']

		# using random.choices()
		# generating random strings
		otcp = ''.join(random.choices(string.ascii_lowercase +string.ascii_uppercase +string.digits, k=37))
		
		email_confirmation = User.objects.filter(email=email).exists()
		if email_confirmation:
			# res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])	
			update_otcp = User.objects.get(email=email)
			update_otcp.otcp = otcp
			update_otcp.save()
			return render(request, 'adminportal/password_reset.html',{"msg":"Request sent, check your email for instructions"})
		else:
			return render(request, 'adminportal/password_reset.html',{"msg":"The email entered is not registered with us!"})
	else:
		return render(request, 'adminportal/password_reset.html')

def password_reset_otcp(request, str):
	if request.method == 'POST':
		new_pswd = request.POST['new_pswd']
		confirm_pswd = request.POST['confirm_pswd']
		profile_otcp = User.objects.get(otcp=str)
		email = profile_otcp.email
		
		if new_pswd != confirm_pswd:
			#messages.info(request, "Password confirmation failed!")	
			context = {
				'msg':'Password confirmation failed!',
				'profile' : profile_otcp
			}
			return render(request, 'adminportal/password_reset_otcp.html', context)

		if len(new_pswd) < 4 or len(new_pswd) > 15:
			context = {
				'msg':'A password should have 4 - 15 characters!',
				'profile' : profile_otcp
			}
			return render(request, 'adminportal/password_reset_otcp.html',context)
			
		else:
			#update password
			user = User.objects.get(email=email)
			user.set_password(new_pswd)
			user.save()

			#delete the otcp from the database after usage
			update_otcp = User.objects.get(email=email)
			update_otcp.otcp = " "
			update_otcp.save()

			messages.info(request, "Password was reset successfuly")	
			return redirect("login-admin")
	else:
		#check whether the link is valid
		confirm_otcp = User.objects.filter(otcp=str).exists()
		if confirm_otcp == False:
			messages.info(request, "Request for a valid password reset link!")	
			return redirect("password-reset-admin")
		else:
			profile_otcp = User.objects.get(otcp=str)
			return render(request, 'adminportal/password_reset_otcp.html',{'profile':profile_otcp})

@login_required(login_url="login-admin")
def adminDashboard(request, *args, **kwargs):
	if request.method == 'POST':
		fname = request.POST['fname']
		mname = request.POST['mname']		
		sname= request.POST['sname']	
		email = request.POST['email']	
		phone= request.POST['phone']
		id_number= request.POST['id_number']
		regno= request.POST['regno']
		family = request.POST['family']
		department = request.POST['department']
		course_title = request.POST['course_title']
		course_name = request.POST['course_name']
		year_of_study = request.POST['year_of_study']

		#id_confirm = profile_detail.objects.filter(id_number=id_number).exists()

		if fname =="":
			messages.info(request, "All the fields marked with * must be filled")	
			return redirect('profile')

		if sname =="":
			messages.info(request, "All the fields marked with * must be filled, you skipped  Sir Name")	
			return redirect('profile')

		if email =="":
			messages.info(request, "All the fields marked with * must be filled, you skipped Email")	
			return redirect('profile')			

		if phone =="":
			messages.info(request, "All the fields marked with * must be filled, you skipped Phone")	
			return redirect('profile')

		if id_number =="":
			messages.info(request, "All the fields marked with * must be filled, you skipped Id number")	
			return redirect('profile')

		if regno == "":
			messages.info(request, "All the fields marked with * must be filled, you skipped Reg No")	
			return redirect('profile')	

		if family == "":
			messages.info(request, "All the fields marked with * must be filled, you did not select a family")	
			return redirect('profile')	
		if department == "":
			messages.info(request, "All the fields marked with * must be filled, you did not select a department")	
			return redirect('profile')	

		if course_title == "":
			messages.info(request, "All the fields marked with * must be filled, you did not select a course title")	
			return redirect('profile')	

		if course_name == "":
			messages.info(request, "All the fields marked with * must be filled, you skipped course name")	
			return redirect('profile')	

		if len(id_number) > 8 or len(id_number) < 8:
			messages.info(request, "A valid id number should have 8 characters!")	
			return redirect('profile')

		if len(phone) > 13 or len(phone) < 10:
			messages.info(request, "A valid phone number should have 10 - 13 characters!")	
			return redirect('profile')


		else:	

			entry = User.objects.get(email=request.user.email)
			entry.first_name = fname
			entry.last_name = mname	
			entry.sir_name = sname
			entry.email =email
			entry.phone = phone
			entry.regno = regno
			entry.id_number = id_number
			entry.family = family
			entry.department = department
			entry.course_title = course_title
			entry.course_name = course_name
			entry.year_of_study = year_of_study

			entry.save()
			messages.info(request, "Profile updated successfully.")	
			return redirect('profile')
	
	else:
		users =User.objects.all()
		men = User.objects.filter(gender='Male').count()
		ladies = User.objects.filter(gender='Female').count()
		user =User.objects.get(email=request.user.email)
		messages = contactUsMessage.objects.all()
		registered = User.objects.all().count()	
		approved = User.objects.filter(is_approved=True).count()
		nonapproved = User.objects.filter(is_approved=False).count()
		st_agnes = User.objects.filter(family='ST. Agnes').count()  
		st_catherine = User.objects.filter(family='ST. Catherine').count()
		st_charles = User.objects.filter(family='ST. Charles').count()
		st_dominic = User.objects.filter(family='ST. Dominic').count()
		st_joseph = User.objects.filter(family='ST. Joseph').count()
		st_jude = User.objects.filter(family='ST. Jude').count()
		st_lucy = User.objects.filter(family='ST. Lucy').count()  
		st_michael = User.objects.filter(family='ST. Michael').count()  
		no_family = User.objects.filter(family='No Family').count()  
		year1 = User.objects.filter(year_of_study='Year 1').count()
		year2 = User.objects.filter(year_of_study='Year 2').count()
		year3 = User.objects.filter(year_of_study='Year 3').count()
		year5 = User.objects.filter(year_of_study='Year 4').count()
		year6 = User.objects.filter(year_of_study='Year 5').count()
		year4 = User.objects.filter(year_of_study='Year 6').count()
		degree = User.objects.filter(course_title='Degree').count()   
		diploma = User.objects.filter(course_title='Diploma').count() 
		certificate = User.objects.filter(course_title='Certificate').count()     
		context = {
			'users':users,
			'user' : user,
			'messages':messages,
			'men':men,
			'ladies':ladies,
			'degree':degree,
			'diploma':diploma,
			'certificate':certificate,
			'registered':registered,
			'st_agnes':st_agnes,
			'st_catherine':st_catherine,
			'st_charles':st_charles,
			'st_dominic':st_dominic,
			'st_joseph':st_joseph,
			'st_jude':st_jude,
			'st_lucy':st_lucy,
			'st_michael':st_michael,	
			'no_family':no_family,
			'year6':year6,
			'year5':year5,
			'year4':year4,
			'year3':year3,
			'year2':year2,
			'year1':year1,
			'approved':approved,
			'nonapproved':nonapproved,
		}
		return render(request, 'adminportal/dashboard.html', context)

@login_required(login_url="login-admin")
def members(request, *args, **kwargs):
	user =User.objects.all().order_by('family')
	context = {
		'users' : user,		
	}
	return render(request, 'adminportal/members.html', context)


@login_required(login_url="login-admin")
def deleteMember(request, str):
	user =User.objects.all()
	delete_user =User.objects.get(id=str)

	context = {
			'users' : user,	
			'msg':'You cannot delete a staff member.',
		}
	if delete_user.is_superuser==True or delete_user.is_staff == True:
		return render(request, 'adminportal/members.html', context)
	else:
		delete_user.delete()
		context = {
			'users' : user,	
			'msg':'Member deleted successfully',
		}
		return render(request, 'adminportal/members.html', context)

@login_required(login_url="login-admin")
def deleteMessage(request, str):
	user =User.objects.all()
	delete_message =contactUsMessage.objects.get(id=str)
	
	delete_message.delete()
	messages.info(request, "Message deleted successfully.")	
	return redirect('admin-dashboard')

@login_required(login_url="login-admin")
def viewMember(request, str):
	view_member = User.objects.get(id=str)	
	context = {
		'user' : view_member,	
	}
	return render(request, 'adminportal/view_member.html', context)

@login_required(login_url="login-admin")
def approveId(request, *args, **kwargs):
	user =User.objects.all().order_by('family')
	context = {
		'users' : user,
	}
	return render(request, 'adminportal/approve_id.html', context)

@login_required(login_url="login-admin")
def approve(request, str):	
	user =User.objects.get(id=str)
	user.is_approved = True
	user.save()	
	return redirect('approve-id')

@login_required(login_url="login-admin")
def unapprove(request, str):	
	user =User.objects.get(id=str)
	user.is_approved = False
	user.save()	
	return redirect('approve-id')

@login_required(login_url="login-admin")	
def generateCsv(request):
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="members.csv"'

	writer = csv.writer(response)
	writer.writerow(['First Name','Middle Name','last Name','Phone','Family','Email','Reg No','Year of Study','Course Title','Course Name','Department', 'Gender'])

	users = User.objects.all().values_list('first_name','last_name','sir_name','phone','family','email','regno','year_of_study','course_title','course_name','department', 'gender')
	for user in users:
		writer.writerow(user)

	return response

@login_required(login_url='login-admin')
def generatePdf(request):
	user = User.objects.get(id=request.user.id)
	if user.is_superuser == False:
		messages.info(request, "You are not allowed to download the pdf.")	
		return redirect('members')
	
	# Create a file-like buffer to receive PDF data.
	buffer = io.BytesIO()

	# Create the PDF object, using the buffer as its "file."
	p = canvas.Canvas(buffer)
	tum_logo = 'media/photos/tum-logo.jpg'

	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	row = 700
	i = 0
	while i < User.objects.all().count():		
		user = User.objects.all().order_by('family')
		p.drawString(200, 750, "TUMCATHCOM MEMBERS LIST")
		p.drawImage(tum_logo, 250, 770, width=100,height=60, preserveAspectRatio=True, mask='auto')
		p.drawString(120, 730, f'First Name {" " " "} Last Name {" " " "} Sir Name {" "} Family {" "} Reg No {" "} Phone')
		p.drawString(90, row, f'{i+1} {" " " "} {user[i].first_name} {" " " "} {user[i].last_name} {" " " "} {user[i].sir_name} {" "} {user[i].family} {" "} {user[i].regno} {" "} {user[i].phone}')
		i += 1
		row = row - 20

	# Close the PDF object cleanly, and we're done.
	p.setTitle("Tumcatcom Members Names List")
	p.setAuthor('Francis Mugambi - +254706046810')
	p.showPage()
	p.save()

	# FileResponse sets the Content-Disposition header so that browsers
	# present the option to save the file.
	buffer.seek(0)
	return FileResponse(buffer, as_attachment=False, filename="members.pdf")


	
@login_required(login_url="login-admin")
def print_id(request, *args, **kwargs):
	user =User.objects.get(email=request.user.email)
	context = {
		'user' : user,
	}
	return render(request, 'portal/print_id.html', context)

def logout(request, *args, **kwargs):
	auth.logout(request)
	return redirect('/')

@login_required(login_url="login-admin")
def votingResults(request):	
	status = authenticateVoting.objects.get(id=1)
	context = {
		'status':status
	}	
	return render(request, 'adminportal/results.html', context)

login_required(login_url="login-admin")
def mainOfficeResults(request):	
	main_office_results = mainOfficeCadidate.objects.all().order_by('post','-votes')
	context = {
		'main_office_results':main_office_results,
	}
	
	return render(request, 'adminportal/main_office_results.html', context)

login_required(login_url="login-admin")
def choirOfficeResults(request):	
	choir_office_results = choirCadidate.objects.all().order_by('post','-votes')
	context = {
		'choir_office_results':choir_office_results,
	}
	
	return render(request, 'adminportal/choir_office_results.html', context)

login_required(login_url="login-admin")
def sccLeadersResults(request):	
	scc_results = sccCadidate.objects.all().order_by('post','-votes')
	context = {
		'scc_results':scc_results,
	}
	
	return render(request, 'adminportal/scc_results.html', context)

login_required(login_url="login-admin")
def cmaClaLeadersResults(request):	
	cma_results = cmaCadidate.objects.all().order_by('post','-votes')
	cla_results = claCadidate.objects.all().order_by('post','-votes')
	context = {
		'cma_results':cma_results,
		'cla_results':cla_results,
	}
	
	return render(request, 'adminportal/cma_cla_results.html', context)


login_required(login_url="login-admin")
def authenticateElection(request):
	allow_voting = authenticateVoting.objects.get(id=1)	
	if allow_voting.is_authenticated_voting == True:
		allow_voting.is_authenticated_voting = False
		allow_voting.save()
		return redirect('voting-results')
	if allow_voting.is_authenticated_voting == False:
		allow_voting.is_authenticated_voting = True		
		allow_voting.save()	
		return redirect('voting-results')	
	return redirect('voting-results')

login_required(login_url="login-admin")
def authenticateEditing(request):
	allow_editing = authenticateVoting.objects.get(id=1)	
	if allow_editing.is_authenticated_editing == True:
		allow_editing.is_authenticated_editing = False
		allow_editing.save()
		return redirect('voting-results')
	if allow_editing.is_authenticated_editing == False:
		allow_editing.is_authenticated_editing = True		
		allow_editing.save()	
		return redirect('voting-results')	
	return redirect('voting-results')