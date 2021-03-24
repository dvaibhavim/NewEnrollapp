from django.shortcuts import render
from django.http import JsonResponse
from Enrollapp.forms import  UserProfileInfoForm
from Enrollapp.models import Schools
# Create your views here.
def register(request):
	#user_form = UserForm()
	profile_form = UserProfileInfoForm()
	#code for autocomplete search used to fetch school name from database
	if 'term' in request.GET:
		qs = Schools.objects.filter(Name__istartswith = request.GET.get('term')) #i stands for case insensitive
		school_name = list() #the url in javascript expects an json response
		for school in qs:
			school_name.append(school.Name)

		return JsonResponse(school_name, safe=False)

	return render(request,'enrollapp/enroll_form.html',
					{#'user_form':user_form,
                           'profile_form':profile_form
                    })
