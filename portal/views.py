from django.shortcuts import render
from django.contrib.auth.models import auth
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from tumcathcom import settings
from .models import User
from .forms import UserForm
from voting.models import family, authenticateVoting
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import random
import string

import reportlab
from reportlab.lib.colors import HexColor
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from django.views import View
# Create your views here.
def login(request, *args, **kwargs):
	if request.method == 'POST':
		email = request.POST['email'].lower()
		password = request.POST['password']

		check_email = User.objects.filter(email=email).exists()
		user = authenticate(request, username=email, password=password)
		
		if email =="":
			return render(request, 'portal/login.html',{"msg1":"Fill the Email field"})

		if password =="":
			return render(request, 'portal/login.html',{"msg1":"Fill the password field"})

		if check_email == False:
			return render(request, 'portal/login.html',{"msg1":"The email does not exist in our database!"})

		if user is  None:
			return render(request, 'portal/login.html',{"msg1":"Invalid Password!"})

		else:
			auth.login(request, user)			
			request.session['semail'] = email  
			return redirect('profile')
			
	else:
		return render(request, 'portal/login.html')
		
def signup(request, *args, **kwargs):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		middle_name = request.POST['middle_name']
		last_name = request.POST['last_name']		
		email = request.POST['email'].lower()
		password = request.POST['password']
		rpt_password = request.POST['rpt_password']

		email_confirm = User.objects.filter(email=email).exists()

		if email =="" or first_name=="" or last_name=="" or middle_name=="" or password=="":
			messages.info(request, " All the fields with * must be filled required!")	
			return redirect('signup')	

		if rpt_password != password:
			messages.info(request, "The passwords did not match!")	
			return redirect('signup')			

		if email_confirm :
			messages.info(request, "A user with that email aready exists")	
			return redirect('signup')

		if len(password) < 4 or len(password) > 15:
			messages.info(request, "A Password should have 4-15 characters!")	
			return redirect('signup')	

		else:
			user =User.objects.create_user(username=email,email=email,first_name=first_name, last_name=middle_name, sir_name=last_name, password=password)
			user.save()			
			messages.info(request, "Account created successfully, please login!")	
			return redirect('login')
	
	else:
		return render(request, 'portal/signup.html')

def password_reset(request, *args, **kwargs):
	if request.method == 'POST':
		email = request.POST['email'].lower()

		# using random.choices()
		# generating random strings
		otcp = ''.join(random.choices(string.ascii_lowercase +string.ascii_uppercase +string.digits, k=37))
		
		email_confirmation = User.objects.filter(email=email).exists()
		if email_confirmation:
			# res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])	
			update_otcp = User.objects.get(email=email)
			update_otcp.otcp = otcp
			update_otcp.save()
			return render(request, 'portal/password_reset.html',{"msg":"Request sent, check your email for instructions"})
		else:
			return render(request, 'portal/password_reset.html',{"msg":"The email entered is not registered with us!"})
	else:
		return render(request, 'portal/password_reset.html')

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
			return render(request, 'portal/password_reset_otcp.html', context)

		if len(new_pswd) < 4 or len(new_pswd) > 15:
			context = {
				'msg':'A password should have 4 - 15 characters!',
				'profile' : profile_otcp
			}
			return render(request, 'portal/password_reset_otcp.html',context)
			
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
			return redirect("login")
	else:
		#check whether the link is valid
		confirm_otcp = User.objects.filter(otcp=str).exists()
		if confirm_otcp == False:
			messages.info(request, "Request for a valid password reset link!")	
			return redirect("password-reset")
		else:
			profile_otcp = User.objects.get(otcp=str)
			return render(request, 'portal/password_reset_otcp.html',{'profile':profile_otcp})
		
@login_required(login_url="login")
def password_change(request, *args, **kwargs):
	if request.method == 'POST':
		old_pswd = request.POST['old_pswd']
		new_pswd = request.POST['new_pswd']
		confirm_new_pswd = request.POST['confirm_new_pswd']
		
		pswd_confirmation = authenticate(request, username=request.user.email, password=old_pswd)
		if old_pswd == "" or new_pswd == "" or confirm_new_pswd == "":
			messages.info(request, "Please fill in all the fields!")	
			return redirect("password-change")

		if pswd_confirmation is None:		
			messages.info(request, "The old password entered is invalid!")	
			return redirect("password-change")

		if len(new_pswd) < 4 or len(new_pswd) > 15:
			messages.info(request, "A password should contain 4 - 15 characters!")	
			return redirect("password-change")

		if new_pswd != confirm_new_pswd:
			messages.info(request, "Password confirmation failed!")	
			return redirect("password-change")

		else:
			user = User.objects.get(email=request.user.email)
			user.set_password(new_pswd)
			user.save()
			messages.info(request, "Password changed successfuly")	
			return redirect("password-change")
	else:
		user =User.objects.get(email=request.user.email)
		context = {
			'user' : user
		}
		return render(request, 'portal/password_change.html', context)

@login_required(login_url="login")
def profile(request, *args, **kwargs):
	if request.method == 'POST':
		fname = request.POST['fname']
		mname = request.POST['mname']		
		sname= request.POST['sname']	
		email = request.POST['email']	
		phone= request.POST['phone']
		id_number= request.POST['id_number']
		regno= request.POST['regno']
		family_name = request.POST['family']
		department = request.POST['department']
		course_title = request.POST['course_title']
		course_name = request.POST['course_name']
		year_of_study = request.POST['year_of_study']
		gender = request.POST['gender']

		#id_confirm = profile_detail.objects.filter(id_number=id_number).exists()

		if fname =="" or gender =="":
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

		if family_name == "":
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
			messages.info(request, "A valid id number should have 8 digits!")	
			return redirect('profile')

		if len(phone) > 13 or len(phone) < 10:
			messages.info(request, "A valid phone number should have 10 - 13 digits!")	
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
			entry.family = family_name
			entry.department = department
			entry.course_title = course_title
			entry.course_name = course_name
			entry.year_of_study = year_of_study
			entry.gender = gender

			entry.save()
			messages.info(request, "Profile updated successfully.")	
			return redirect('profile')
	
	else:
		familys = family.objects.all()
		user =User.objects.get(email=request.user.email)
		authenticate_editing = authenticateVoting.objects.get(id=1)	
		context = {
			'user' : user,
			'familys':familys,
			'authenticate_editing':authenticate_editing,
		}
		return render(request, 'portal/profile.html', context)

@login_required(login_url="login")
def leaders(request, *args, **kwargs):
	user =User.objects.get(email=request.user.email)
	context = {
		'user' : user,		
	}
	return render(request, 'portal/leaders.html', context)

@login_required(login_url="login")
def print_id(request, *args, **kwargs):
	user =User.objects.get(email=request.user.email)
	if user.first_name == "" or user.sir_name =="" or user.phone=="" or user.id_number=="" or user.regno=="":
		messages.info(request, "You cannot print id before updating all your Profile details below.")
		return redirect('profile')	
	context = {
		'user' : user,
	}
	return render(request, 'portal/print_id.html', context)
	
@login_required(login_url="login")
def requestApproval(request, str):	
	user =User.objects.get(id=str)
	user.has_request = True
	user.save()	
	return redirect('print-id')

@login_required(login_url="login")
def news_events(request, *args, **kwargs):
	user =User.objects.get(email=request.user.email)
	context = {
		'user' : user
	}
	return render(request, 'portal/news_events.html', context)
	

def logout(request, *args, **kwargs):
	auth.logout(request)
	return redirect('/')

@login_required(login_url='login')
def updateProfilePicture(request):
	user = request.user
	form = UserForm(instance=user)

	if request.method == 'POST':
		
		form = UserForm(request.POST, request.FILES, instance=user)
		if request.FILES == "":
			return render(request, 'portal/update_profile_picture.html', {'msg':'You have not choosen an image!.'})
		if form.is_valid():
			form.save()
			return render(request, 'portal/update_profile_picture.html', {'msg':'Profile picture updated successfuly.'})

	else:
		return render(request, 'portal/update_profile_picture.html')

@login_required(login_url='login')
def downloadCard(request, str):
	user = User.objects.get(id=str)
	users = User.objects.all()
	if user.is_approved == False:
		messages.info(request, "You have not been approved to download the id.")	
		return redirect('print-id')
	if user.photo == "photos/default-profile.png":
		messages.info(request, "You cannot download id before updating your Profile picture.")
		return redirect('print-id')
	tum_logo = 'media/photos/tum-logo.jpg'
	my_profile = f'media/{user.photo}'
	# Create a file-like buffer to receive PDF data.
	buffer = io.BytesIO()

	# Create the PDF object, using the buffer as its "file."
	p = canvas.Canvas(buffer)
	p.setFillColorRGB(0.4,0,0)
	p.setTitle("Membership card")
	#canvas.rect(left_padding, bottom_padding, width, height, fill=1)
	p.rect(0,685,245,157,fill=1)
	p.setFillColor(HexColor("#f5f5f5"))

	p.setFontSize(7)
	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	p.drawString(67, 820, "Technical University" )
	p.drawString(72, 810, "of Mombasa" )
	p.drawString(140, 820, "Tumcathcom membership card" )
	p.drawString(140, 800, "Serial Number: " f'{user.id_number}{user.id}' )
	p.drawString(80, 775, "Id Number:" )
	p.drawString(80, 760, f'{user.id_number}' )
	p.drawString(150, 775, "Full Name:" )
	p.drawString(150, 760, f'{user.first_name} {user.last_name} {user.sir_name}' )
	p.drawString(80, 730, "Reg No: " f'{user.regno}')	
	p.drawString(80, 710, "Family: " f'{user.family}')
	p.drawImage(tum_logo, 18, 780, width=40,height=50, preserveAspectRatio=True, mask='auto')
	p.drawImage(my_profile, 10, 700, width=60,height=70, preserveAspectRatio=True, mask='auto')
		

	# Close the PDF object cleanly, and we're done.
	p.showPage()
	p.save()

	# FileResponse sets the Content-Disposition header so that browsers
	# present the option to save the file.
	buffer.seek(0)
	return FileResponse(buffer, as_attachment=True, filename=f'{user.first_name}.pdf')

@login_required(login_url="login")
def printCard(request, str):
	user = User.objects.get(id=str)
	if user.is_approved == False:
		messages.info(request, "You have not been approved to print the id.")
		return redirect('print-id')
	
	if user.photo == "photos/default-profile.png":
		messages.info(request, "You cannot print id before updating your Profile picture.")
		return redirect('print-id')

	tum_logo = 'media/photos/tum-logo.jpg'
	my_profile = f'media/{user.photo}'

	# Create a file-like buffer to receive PDF data.
	buffer = io.BytesIO()

	# Create the PDF object, using the buffer as its "file."
	p = canvas.Canvas(buffer)
	p.setFillColorRGB(0.4,0,0)
	p.setTitle(f'{user.first_name} Tumcathcom Membership Card')
	p.setSubject(f'This card was generated for {user.first_name} {user.sir_name}.') 
	#canvas.rect(left_padding, bottom_padding, width, height, fill=1)
	p.roundRect(0,685,250,157,5,stroke=0, fill=1)
	p.setFillColor(HexColor("#f5f5f5"))
	p.setFontSize(7)
	p.setAuthor('Francis Mugambi - +254706046810')
	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	p.drawString(67, 820, "Technical University" )
	p.drawString(72, 810, "of Mombasa" )
	p.drawString(140, 820, "Tumcathcom membership card" )
	p.drawString(140, 808, "Serial Number: " f'{user.id_number}{user.id}' )
	p.drawString(80, 775, "Id Number:" )
	p.drawString(80, 760, f'{user.id_number}' )
	p.drawString(150, 775, "Full Name:" )
	p.drawString(150, 760, f'{user.first_name} {user.last_name} {user.sir_name}' )
	p.drawString(80, 730, "Reg No: " f'{user.regno}')	
	p.drawString(80, 710, "Family: " f'{user.family}')
	p.drawImage(tum_logo, 18, 780, width=40,height=50, preserveAspectRatio=True, mask='auto')
	p.drawImage(my_profile, 10, 700, width=60,height=70, preserveAspectRatio=True, mask='auto')
		

	# Close the PDF object cleanly, and we're done.
	p.showPage()
	p.save()

	# FileResponse sets the Content-Disposition header so that browsers
	# present the option to save the file.
	buffer.seek(0)
	return FileResponse(buffer, as_attachment=False, filename=f'{user.first_name} Tumcathcom Id Card.pdf')




from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.colors import Color, black, blue, red
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab import platypus
@login_required(login_url="login")
def generateCV(request, str):
	user = User.objects.get(id=str)
	if user.is_approved == False:
		messages.info(request, "You have not been approved to print the id.")
		return redirect('print-id')
	
	if user.photo == "photos/default-profile.png":
		messages.info(request, "You cannot print id before updating your Profile picture.")
		return redirect('print-id')

	tum_logo = 'media/photos/tum-logo.jpg'
	my_profile = f'media/{user.photo}'
	styles = getSampleStyleSheet()
	styleN = PS(name = 'Normal',
				fontSize = 10,
				leading = 14,
				firstLineIndent=-5,
				)
	stylePhoto = PS(name = 'Normal',
				fontSize = 10,
				leading = 84,
				firstLineIndent=25,
				)
	styleS = PS(name = 'Normal',
				fontSize = 12,
				leading = 22,	
				leftPadding=6			
				)
	styleName = PS(name = 'Normal',
				fontSize = 12,
				leading = 32,				
				firstLineIndent=0,		
				)
	styleP = PS(name = 'Normal',				
				leftPadding=16			
				)
	styleF = PS(name = 'Normal',				
				leading = 40,				
				)
	normal = PS(name = 'Normal',				
				leading = 15,				
					
				)
	styleH = styles['Heading3']
	styleH3 = styles['Heading4']
	styleH5 = styles['Heading5']
	styleH6 = PS(name = 'Heading6',
				fontSize = 10,
				leading = 14,
				firstLineIndent=-5,
				)
	styleHIdent = PS(name = 'Normal',				
				firstLineIndent=0,
				)

	#side sestion
	profile =  []
	#TITLE
	email = '<link href="' + 'mailto:francismugambi97@gmail.com' + '">'+ "<font color=white ><img height=12 width=10 src='media/photos/email.png' valign='top'/> francismugambi97@gmail.com</font>"+ '</link>'
	web = '<link href="' + 'http://www.francis-mugambi.me.ke' + '">'+ "<font color=white ><img height=12 width=10 src='media/photos/web.png' valign='top'/> francis-mugambi.me.ke</font>"+ '</link>'
	linkedin = '<link href="' + 'http://www.linkedin.com/in/francis-mugambi' + '">'+ "<font color=white ><img height=12 width=10 src='media/photos/linkedin.png' valign='top'/> linkedin.com/in/francis-mugambi</font>"+ '</link>'
	github = '<link href="' + 'http://www.github.com/francis-mugambi' + '">'+ "<font color=white ><img height=12 width=10 src='media/photos/github.png' valign='top'/> github.com/francis-mugambi</font>"+ '</link>'
	
	#profile.append(Paragraph("<font color=white ><img height=72 width=90 src='media/photos/myprofile.jpg' valign='top'/></font>",stylePhoto))
	profile.append(Paragraph("<font color=white size=23 name=Times-Roman>Francis Mugambi</font>",styleName))
	profile.append(Paragraph("<font color=white size=14>Back End Developer</font>", styleF))
	#contacts
	
	#story.append(Paragraph("<para borderRadius = 150></para> ",styleH))
	profile.append(Paragraph("<font color=white size=15>CONTACTS</font>",styleS))
	profile.append(Paragraph(f"<font color=white ><img height=12 width=10 src='media/photos/location.png' valign='top'/> Kerugoya, Kenya, 44-10300</font>",styleS))
	profile.append(platypus.Paragraph(email, styleS))	
	profile.append(Paragraph(f"<font color=white ><img height=12 width=10 src='media/photos/phone.png' valign='top'/> +254706046810</font>",styleS))
	profile.append(platypus.Paragraph(web, styleS))
	profile.append(platypus.Paragraph(linkedin, styleS))
	profile.append(platypus.Paragraph(github, styleF))

	#education
	# profile.append(Paragraph("<font color=white size=15>EDUCATION</font>",styleS))
	# profile.append(Paragraph("<font color=white size=11>Bachelor of Science in Mathematics and Computer Science</font>",styleS))
	# profile.append(Paragraph("<font color=white size=9>Technical University of Mombasa</font>",styleS))
	# profile.append(Paragraph("<font color=white size=8>09/2018 - 07/2023</font>",styleF))
	#SKILLS
	profile.append(Paragraph("<font color=white size=15>TECHNICAL SKILLS</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>HTML, CSS, Bootstrap</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Python, PHP, Ruby, JavaScript</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Django, Rails</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>MYSQL, Oracle</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>API's, Docker, OOP, Agile, SEO</font>",styleS))
	#profile.append(Paragraph("<font color=white size=10>MS-Word, MS-Excel, MS-Acess, MS-Publisher, MS-Publisher</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Git, Github</font>",styleF))
	#SOFT SKILLS
	profile.append(Paragraph("<font color=white size=15>SOFT SKILLS</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Strong Analytical skills</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Team player and problem solver</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Goal oriented and Self-motivated </font>",styleS))	
	profile.append(Paragraph("<font color=white size=10>High level of integrity</font>",styleS))	
	profile.append(Paragraph("<font color=white size=10>Professionalism</font>",styleS))	
	
	profile.append(Paragraph("<font color=white size=10>Strong verbal and communication skills</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Excellent time management</font>",styleF))
	#INTERESTS
	profile.append(Paragraph("<font color=white size=15>INTERESTS</font>",styleS))	
	profile.append(Paragraph("<font color=white size=10>Software Development</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Machine Leaning</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Data Science</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Artificial Inteligence</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Banking and Finance</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Participating in social activities</font>",styleS))
	profile.append(Paragraph("<font color=white size=10>Online Surfing</font>",styleS))
	
	#add some flowables
	story = []
	#story.append(Paragraph("<para borderRadius = 150><img height=22 width=45 src='media/photos/myprofile.jpg' valign='top'/></para> ",styleH))
	#career Summary
	story.append(Paragraph("<font>CAREER PROFILE</font> ",styleH))
	story.append(Paragraph("Francis Mugambi is a Back-end developer with a strong passion for using technology to solve problems. He is proficient in Python programming language, PHP, MYSQL database and Django framework. He is eager to continue learning and growing as a web developer. He enjoys staying up to date with the latest technology trends. He is team player and is excited to contribute his skills and knowledge to any project.",
	normal))
	#experiences
	story.append(Paragraph("<font>EXPERIENCE</font>",styleH))
	#experience 1
	story.append(Paragraph("Full Stack Developer, Volunteer",styleH3))
	story.append(Paragraph("<i>Technical University of Mombasa Catholic Community.</i>",styleH5))
	story.append(Paragraph("<font size=9><i>Feb 2023 - present</i></font>",styleH5))	
	story.append(Paragraph("- Developing and maintaining all the systems.",
	styleH6))
	story.append(Paragraph("- Checking and fixing the emerging bugs in the systems.",
	styleH6))
	story.append(Paragraph("- Provide support to the students and staff members when using the systems.",
	styleH6))
	story.append(Paragraph("- Monitor the website to find out solutions to be implemented to improve it's speed and SEO using google analytics and google console tools.",
	styleH6))
	story.append(Paragraph("- Designed, created and deployed a new modern and responsive website.",
	styleH6))
	story.append(Paragraph("- Developed and implemented members registration portal, a voting system and an admin dashboard using django framework.",
	styleH6))
	#experience 2
	story.append(Paragraph("Full Stack Developer",styleH3))
	story.append(Paragraph("<i>Freelancing</i>",styleH5))
	story.append(Paragraph("<font size=9><i>Feb 2022 - May 2023</i></font>",styleH5))
	story.append(Paragraph("- Developed a responsive website for Tecsol company using Bootstrap, JavaScript and PHP.",
	styleN))
	story.append(Paragraph("- Created and deployed a gaming web application using JavaScript and Django framework.",
	styleN))
	#experience 3
	story.append(Paragraph("<font>PROJECTS</font>",styleH))
	story.append(Paragraph("<b> Resume writter</b>, designed and developed a resume writter application using Django framework.",
	normal))
	story.append(Paragraph("<b> Career guide system</b>, developed and implemented a career guide system for the students using django framework.",
	normal))
	story.append(Paragraph("<b> Web Development school</b>, developed and implementend an online web development tutorial school using Django framework and Bootstrap.",
	normal))
	story.append(Paragraph("<b> Ecommerce website</b>, created an ecommerce website using Bootstrap, PHP and MYSQL database .",
	normal))
	story.append(Paragraph("<b>Voting system</b>, designed, developed and implemented an online voting system using python, django framework.",
	normal))
	story.append(Paragraph("<b>Members registration portal</b>, created an application for registering and generating membership identity card.",
	normal))
	
	#Education
	story.append(Paragraph("<font color=black>EDUCATION</font>",styleH))
	story.append(Paragraph("<b><font size=9.5>Bachelor of Science in Mathematics and Computer Science (Statistics Option)</font></b>",
	styleHIdent))
	story.append(Paragraph("Techical University of Mombasa",
	styleHIdent))
	story.append(Paragraph("<i>Sep 2018 - Dec 2022</i>",	styleHIdent))
	#professional courses
	story.append(Paragraph("<font>COMPLETED PROFESSIONAL COURSES</font>",styleH))
	story.append(Paragraph("Complete Python Programming Course Beginner to Advanced (Udemy).",
	normal))
	story.append(Paragraph("Databases for Developers Foundations (Oracle Dev Gym)",
	normal))
	story.append(Paragraph("Search Engine Optimization Complete Specialization Course (Udemy).",
	normal))
	story.append(Paragraph("Scrum Certification Course (Udemy).",	normal))
	story.append(Paragraph("Docker from scratch Course (Udemy).",	normal))
	story.append(Paragraph("Ruby programming language Course (Sololern).",	normal))
	#Others
	story.append(Paragraph("<font color=black>Others</font>",styleH))
	story.append(Paragraph("<b><font size=10>Certification in Microsoft computer packages</font></b>",
	styleHIdent))
	story.append(Paragraph("St. Andrew's College of Theology & Development, Kabare",
	styleHIdent))
	story.append(Paragraph("Excel, Access, Word, Publisher & PowerPoint",
	styleHIdent))
	#references
	# story.append(Paragraph("<font>REFERENCES</font>",styleH))
	# story.append(Paragraph("Dr Kennedy Khadullo",styleN))
	# story.append(Paragraph("Technical University of Mombasa",styleN))
	# story.append(Paragraph("University Lecturer",styleN))
	# story.append(Paragraph("Phone: +254733770772",styleN))
	# story.append(Paragraph("Email: khadullo@gmail.com",styleN))
	# #others
	# reference = []
	# #reference.append(Paragraph('REFERENCES',styleH))

	# reference.append(Paragraph("Eliud Muigu",styleN))
	# reference.append(Paragraph("Kenya Revenue Authority",styleN))
	# reference.append(Paragraph("KRA Officer",styleN))
	# reference.append(Paragraph("Phone: +254722844588",styleN))
	# reference.append(Paragraph("Email: muigue43@gmail.com",styleN))
	
	# Create a file-like buffer to receive PDF data.
	buffer = io.BytesIO()

	# Create the PDF object, using the buffer as its "file."
	p = canvas.Canvas(buffer)
	#p.setFillColorRGB(0.3,0.54,0.6)
	#p.setFillColorRGB(0.12,0.576,1)
	#p.setFillColorRGB(0.12,0.576,0.6)
	p.setFillColorRGB(0.12,0.176,0.34)
	#p.setFillColorRGB(0.52,0.276,0.99)
	#p.setFillColorRGB(0.180,0.5255,0.75686)
	p.setTitle(f'{user.first_name} {user.last_name} Resume')
	p.setSubject(f'This resume was generated for {user.first_name} {user.sir_name}.') 
	#canvas.rect(left_padding, bottom_padding, width, height, fill=1)
	p.rect(0,0,205,850, stroke=0, fill=1)

	p.setFillColor(HexColor("#f5f5f5"))
	p.setFontSize(17)
	p.setAuthor('Francis Mugambi - +254706046810')
	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	#p.drawString(20, 700, "Francis Mugambi" )
	#p.drawString(20, 680, "Back End Developer" )
	# p.drawString(140, 820, "Tumcathcom membership card" )
	# p.drawString(140, 808, "Serial Number: " f'{user.id_number}{user.id}' )
	# p.drawString(80, 775, "Id Number:" )
	# p.drawString(80, 760, f'{user.id_number}' )
	# p.drawString(150, 775, "Full Name:" )
	# p.drawString(150, 760, f'{user.first_name} {user.last_name} {user.sir_name}' )
	# p.drawString(80, 730, "Reg No: " f'{user.regno}')	
	# p.drawString(80, 710, "Family: " f'{user.family}')
	f = Frame(215, 0, 377,820, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
	c = Frame(10, 0, 195,840, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
	d = Frame(420, 0, 377,130, leftPadding=6, bottomPadding=6,rightPadding=6, topPadding=6, id=None, showBoundary=0)
	f.addFromList(story,p)
	c.addFromList(profile,p)
	#d.addFromList(reference,p)
	# p.drawImage(tum_logo, 18, 780, width=40,height=50, preserveAspectRatio=True, mask='auto')
	#p.drawImage(my_profile, 35, 730, width=110,height=90, preserveAspectRatio=True, mask='auto')
	#p.circle(90, 794, 43, stroke=1, fill=0)	

	# Close the PDF object cleanly, and we're done.
	p.showPage()
	p.save()

	# FileResponse sets the Content-Disposition header so that browsers
	# present the option to save the file.
	buffer.seek(0)
	return FileResponse(buffer, as_attachment=False, filename=f'{user.first_name} Resume.pdf')