from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Schools(models.Model):
	Name = models.CharField(max_length=500)
	Reg_no = models.CharField(max_length=50)

	def __str__(self):
		return self.Name

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	firstname = models.CharField(max_length=20)
	lastname = models.CharField(max_length=20)
	gender = models.CharField(max_length=10)
	date_of_birth = models.CharField(max_length=20)
	Role = models.CharField(max_length=20)
	standard = models.CharField(max_length=4)
	sis_id = models.IntegerField(default=1)
	school_name = models.ForeignKey(Schools, on_delete=models.CASCADE)


