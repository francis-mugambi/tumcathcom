from django.db import models
from portal.models import User

#Model for main office posts
class mainOfficePost(models.Model):
    post_name = models.CharField( max_length=150, unique=True);  

    def __str__(self):
        return self.post_name 
#Model for choir posts
class choirPost(models.Model):
    post_name = models.CharField( max_length=150, unique=True);  

    def __str__(self):
        return self.post_name 
#Model for CMA posts
class cmaPost(models.Model):
    post_name = models.CharField( max_length=150, unique=True);  

    def __str__(self):
        return self.post_name 
#Model for CLA posts
class claPost(models.Model):
    post_name = models.CharField( max_length=150, unique=True);  

    def __str__(self):
        return self.post_name 
#Model for SCC posts
class sccPost(models.Model):
    post_name = models.CharField( max_length=150, unique=True);  

    def __str__(self):
        return self.post_name 
#Model for familes
class family(models.Model):
    family_name = models.CharField( max_length=150, unique=True);  

    def __str__(self):
        return self.family_name 

#Model for main office cadidates
class mainOfficeCadidate(models.Model):
    post = models.ForeignKey(mainOfficePost, on_delete=models.CASCADE);
    cadidate_name = models.CharField( max_length=100, unique=True);   
    cadidate_photo = models.ImageField(upload_to='main_office_cadidates', default='default-profile.png');
    votes = models.IntegerField(default=0);

    def __str__(self):
        return self.post.post_name +" ==> "+ self.cadidate_name

    class Meta:
        ordering:['post']
#Model for choir office cadidates
class choirCadidate(models.Model):
    post = models.ForeignKey(choirPost, on_delete=models.CASCADE);
    cadidate_name = models.CharField( max_length=100, unique=True);    
    cadidate_photo = models.ImageField(upload_to='choir_cadidates', default='default-profile.png');
    votes = models.IntegerField(default=0);

    def __str__(self):
        return self.post.post_name +" ==> "+ self.cadidate_name
    class Meta:
        ordering:['-post']
    # class __init__(self, *args, **kwargs):
    #     super(choirCadidate, self).__init__(*args, **kwargs)
    #     self.fields['post'].empty_label = "select"
#Model for CMA cadidates
class cmaCadidate(models.Model):
    post = models.ForeignKey(cmaPost, on_delete=models.CASCADE);
    cadidate_name = models.CharField( max_length=100, unique=True);   
    cadidate_photo = models.ImageField(upload_to='cma_cadidates', default='default-profile.png');
    votes = models.IntegerField(default=0);

    def __str__(self):
        return self.post.post_name +" ==> "+ self.cadidate_name
    class Meta:
        ordering:['-post']
#Model for CLA cadidates   
class claCadidate(models.Model):
    post = models.ForeignKey(claPost, on_delete=models.CASCADE);
    cadidate_name = models.CharField( max_length=100, unique=True);    
    cadidate_photo = models.ImageField(upload_to='cla_cadidates', default='default-profile.png');
    votes = models.IntegerField(default=0);

    def __str__(self):
        return self.post.post_name +" ==> "+ self.cadidate_name
    class Meta:
        ordering:['-post']
#Model for SCC cadidates
class sccCadidate(models.Model):
    family = models.ForeignKey(family, on_delete=models.CASCADE);  
    post = models.ForeignKey(sccPost, on_delete=models.CASCADE);
    cadidate_name = models.CharField( max_length=100, unique=True);      
    cadidate_photo = models.ImageField(upload_to='scc_cadidates', default='default-profile.png');
    votes = models.IntegerField(default=0);

    def __str__(self):
        return self.family.family_name +" ==> "+self.post.post_name +" ==> "+ self.cadidate_name
    class Meta:
        ordering:['family','post']
    
class authenticateVoting(models.Model):
    is_authenticated_voting = models.BooleanField(default=False)
    is_authenticated_editing = models.BooleanField(default=False)
    # def __str__(self):
    #     return self.is_authenticated_voting

#Model for registering voters    
class voter(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    #main office
    voted_office_chairperson = models.BooleanField(default=False)
    voted_vice_chairperson = models.BooleanField(default=False)
    voted_office_secretary = models.BooleanField(default=False)
    voted_vice_secretary = models.BooleanField(default=False)
    voted_office_treasurer = models.BooleanField(default=False)
    voted_asset_manager = models.BooleanField(default=False)
    voted_scc_leader = models.BooleanField(default=False)
    voted_organizing_secretary = models.BooleanField(default=False)
    voted_hospitality_manager = models.BooleanField(default=False)
    voted_Liturgical_leader = models.BooleanField(default=False)
    #choir office
    voted_choir_chairperson = models.BooleanField(default=False)    
    voted_choir_secretary = models.BooleanField(default=False)    
    voted_choir_treasurer = models.BooleanField(default=False)
    voted_choir_director = models.BooleanField(default=False)
    voted_asst_choir_director = models.BooleanField(default=False)
    voted_dancers_coordinator = models.BooleanField(default=False)
    voted_dancers_secretary = models.BooleanField(default=False)
    voted_worship_coordinator = models.BooleanField(default=False)    
    #CMA & CLA
    voted_cma_chairperson = models.BooleanField(default=False)    
    voted_cma_secretary = models.BooleanField(default=False)   
    #
    voted_cla_chairperson = models.BooleanField(default=False)    
    voted_cla_secretary = models.BooleanField(default=False)   
    #scc leaders 
    voted_family_chairperson = models.BooleanField(default=False)
    voted_project_manager = models.BooleanField(default=False)
    voted_family_secretary = models.BooleanField(default=False)

    def __str__(self):
        return self.name.first_name +" "+ self.name.sir_name

    