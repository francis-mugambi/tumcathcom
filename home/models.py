from django.db import models
from voting.models import family, mainOfficePost, choirPost, sccPost, cmaPost, claPost

# Create your models here.
class contactUsMessage(models.Model):
    name = models.CharField(max_length=100);
    email = models.EmailField(max_length=20);
    subject = models.CharField(max_length=100);
    message = models.TextField(max_length=500);

    def __str__(self):
        return self.subject

class NameField(models.CharField):

    def get_prep_value(self, value):
        return str(value).lower()

class blog(models.Model):
    blog_title = NameField(max_length=100, unique=True,  help_text='Blog title should no exceed 10 words. Comas are not allowed');
    blog_body = models.TextField(); 
    photo = models.ImageField(upload_to='blogs_photos', default='bible.jpeg', blank=True)   
    def __str__(self):
        return self.blog_title

    def human_readable_state(self):
        return self.blog_title.replace('-', ' ')

class familiesPhoto(models.Model):
    family_name = models.ForeignKey(family, on_delete=models.CASCADE);
    photo = models.ImageField(upload_to='family_photos')
    def __str__(self):
        return self.family_name.family_name

class eventsPhoto(models.Model):
    caption = models.TextField();
    photo = models.ImageField(upload_to='events_photos')
    def __str__(self):
        return self.caption[0:50]


class mainOfficeLeader(models.Model):
    post = models.ForeignKey(mainOfficePost, on_delete=models.CASCADE);
    leader_name = models.CharField(max_length=100);    
    photo = models.ImageField(upload_to='leadership/main_office_leaders', default='default-profile.png');
    def __str__(self):
        return self.post.post_name +" "+ self.leader_name

class choirOfficeLeader(models.Model):
    post = models.ForeignKey(choirPost, on_delete=models.CASCADE);
    leader_name = models.CharField(max_length=100);    
    photo = models.ImageField(upload_to='leadership/choir_office_leaders', default='default-profile.png');
    def __str__(self):
        return self.post.post_name +" "+ self.leader_name

class sccLeader(models.Model):    
    family = models.ForeignKey(family, on_delete=models.CASCADE);
    post = models.ForeignKey(sccPost, on_delete=models.CASCADE);
    leader_name = models.CharField(max_length=100);
    photo = models.ImageField(upload_to='leadership/scc_leaders', default='default-profile.png');
    class Meta:
        ordering:['family']
    def __str__(self):
        return self.family.family_name +" ===>"+ self.post.post_name +"===> "+ self.leader_name

class cmaLeader(models.Model):
    post = models.ForeignKey(cmaPost, on_delete=models.CASCADE);
    leader_name = models.CharField(max_length=100);    
    photo = models.ImageField(upload_to='leadership/cma_leaders', default='default-profile.png');
    def __str__(self):
        return self.post.post_name +" "+ self.leader_name

class claLeader(models.Model):
    post = models.ForeignKey(claPost, on_delete=models.CASCADE);
    leader_name = models.CharField(max_length=100);    
    photo = models.ImageField(upload_to='leadership/cla_leaders', default='default-profile.png');
    def __str__(self):
       return self.post.post_name +" "+ self.leader_name

