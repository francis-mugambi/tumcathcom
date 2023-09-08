from django.contrib import admin

from .models import contactUsMessage, mainOfficeLeader, choirOfficeLeader, sccLeader, cmaLeader, claLeader, blog, eventsPhoto, familiesPhoto

# Register your models here.
# admin.site.register(contactUsMessage)
admin.site.register(mainOfficeLeader)
admin.site.register(choirOfficeLeader)
admin.site.register(sccLeader)
admin.site.register(claLeader)
admin.site.register(cmaLeader)
admin.site.register(blog)
admin.site.register(eventsPhoto)
admin.site.register(familiesPhoto)