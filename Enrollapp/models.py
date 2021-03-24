from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	firstname = models.CharField(max_length=20)
	lastname = models.CharField(max_length=20)
	GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	date_of_birth = models.DateField(max_length=8)
	User_type_choices = (('Student','Student'),('Parent','Parent'), ('Teacher','Teacher'),('Administrator','Administrator'))
	Role = models.CharField(choices=User_type_choices,max_length=20)
	CLASS_CHOICES = (('8','Class 8'),('9','Class 9'),('10','Class 10'),('11','Class 11'),('12','Class 12'))
	standard = models.CharField(max_length=4, choices=CLASS_CHOICES)

class Schools(models.Model):
	Name = models.CharField(max_length=500)
	Reg_no = models.CharField(max_length=50)

	def __str__(self):
		return self.Name