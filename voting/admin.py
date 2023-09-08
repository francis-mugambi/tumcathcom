from django.contrib import admin
from .models import voter, mainOfficeCadidate, choirCadidate,sccCadidate, cmaCadidate, claCadidate
from .models import mainOfficePost, choirPost, cmaPost, claPost, sccPost, family, authenticateVoting
# Register your models here.
#admin.site.register(voter)
admin.site.register(mainOfficeCadidate)
admin.site.register(choirCadidate)
admin.site.register(sccCadidate)
admin.site.register(cmaCadidate)
admin.site.register(claCadidate)
admin.site.register(mainOfficePost)
admin.site.register(choirPost)
admin.site.register(cmaPost)
admin.site.register(claPost)
admin.site.register(sccPost)
admin.site.register(family)
# admin.site.register(authenticateVoting)