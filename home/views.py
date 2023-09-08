from django.shortcuts import render,redirect
from tumcathcom import urls
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import contactUsMessage, mainOfficeLeader, familiesPhoto, eventsPhoto, blog, sccLeader

# Create your views here.
def home(request, *args, **kwargs):
	return render(request, 'home/index.html')

def blogs(request):
	blog_iteams = blog.objects.all()
	blog_urls = blog.objects.all()
	for blog_url in blog_urls:
	 	blog_url.blog_title = blog_url.blog_title.replace(' ', '-')
	context = {
		'blogs':blog_iteams,
		'blog_urls':blog_urls,
	}
	return render(request, 'home/blogs.html', context)

def blogIteam(request, str):
	str = str.replace('-', ' ')
	blog_iteam = blog.objects.get(blog_title=str)
	context = {
		'blog':blog_iteam,
	}
	return render(request, 'home/blog.html', context)

def leadership(request, *args, **kwargs):
	leaders = mainOfficeLeader.objects.all()
	context = {
		'leaders':leaders
	}
	return render(request, 'home/leadership.html', context)

def scc_leaders(request, *args, **kwargs):
	leaders = sccLeader.objects.all().order_by('family','post')
	context = {
		'leaders':leaders
	}
	return render(request, 'home/scc_leaders.html',context)

def photos(request, *args, **kwargs):
	families_photos = familiesPhoto.objects.all().order_by('family_name')
	events_photos = eventsPhoto.objects.all()
	context = {
		'families_photos':families_photos,
		'events_photos':events_photos,
	}
	return render(request, 'home/photos.html', context)

def videos(request, *args, **kwargs):
	return render(request, 'home/videos.html')

def contact(request, *args, **kwargs):
	if request.method == 'POST':
		recaptcha = request.POST['recaptcha']
		name = request.POST['name']
		email = request.POST['email'].lower()
		subject = request.POST['subject']
		message = request.POST['message']
		message_exist = contactUsMessage.objects.filter(name=name,email=email,subject=subject,message=message).exists()

		if email =="" or email =="" or subject =="" or message =="" or recaptcha =="":
			messages.info(request, " All the fields are required")	
			return redirect('/contacts/')

		if len(name) < 3 or len(email) < 3 or len(subject) < 3 or len(message) < 3:
			messages.info(request, "The message was not sent!")	
			return redirect('/contacts/')
		if recaptcha != "10":
			messages.info(request, "Message not sent, You failed the recaptcha test!")	
			return redirect('/contacts/')				

		if message_exist:
			messages.info(request, "We have aready received your message")	
			return redirect('/contacts/')

		else:
			save_message = contactUsMessage.objects.create(name=name,email=email, subject=subject, message=message)
			save_message.save()
			messages.info(request, "Message sent, thank you for contacting us")	
			return redirect('/contacts/')
	
	else:
		return render(request, 'home/contact.html')