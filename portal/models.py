from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    gender_type = [("Male","Male"), ("Female","Female")]    
    sir_name = models.CharField('Middle Name', max_length=70, blank=True);
    gender = models.CharField(max_length=6, choices=gender_type)
    phone = models.CharField(max_length=20);
    regno = models.CharField(max_length=20);
    id_number = models.CharField(max_length=10);
    department = models.CharField(max_length=150);
    family = models.CharField(max_length=50);
    department = models.CharField(max_length=150);    
    course_title = models.CharField(max_length=50);
    course_name = models.CharField(max_length=150);
    year_of_study = models.CharField(max_length=10, blank=True, null=True);
    otcp = models.CharField(max_length=50, blank=True, null=True);
    is_approved = models.BooleanField(default=False)
    has_request = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="photos", default='default-profile.png', blank=False);
    USER_NAME_FIELD = 'email'

    def __str__(self):
        return self.email

