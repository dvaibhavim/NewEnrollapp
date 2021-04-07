from django.shortcuts import render
from django.http import JsonResponse
from Enrollapp.forms import  UserProfileInfoForm
from Enrollapp.models import Schools
from canvasapi import Canvas

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
   
    return render(request,'enrollapp/Enroll_form_Nagaed_Digital.html',
                    {'profile_form':profile_form})





"""function to create new user and send registration email. If the account gets created, course is also assigned to the student. """
def create_account(request):
         #Canvas Api Url
    API_URL = "https://learn.nagaed.com/"
    # Canvas API key
    API_KEY = "puoPtPQS1lGkhuaPEhmTreh2MZTtj1clp4OEiZ1UVVpugZBOn76WBue5Zf3MKBl5"    
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)
    if request.method=="POST":
        account = canvas.get_account(1)
        #sis_user_id generation logic
        user_Canvas = account.create_user(
                    user={
                        'name': request.POST.get("q56_name[first]")+" "+ request.POST.get("q56_name[last]"), # profile.firstname + " " + profile.lastname,
                        'skip_registration': False
                    },
                    pseudonym={                        
                        'sis_user_id': 'vd_test',
                        'unique_id' :request.POST.get("q55_emailAddress"),
                        'send_confirmation':True,
                        'address':request.POST.get("q55_emailAddress")
                        },
                    communication_channel={
                        'type': 'email',
                        'skip_confirmation': False
                    }
                )
        school_name = request.POST.get("schoolname")
        sub_accounts =  account.get_subaccounts()
        for accounts in sub_accounts:
            if accounts.lower() == school_name.lower():
                sub_account = accounts
        
        #logic to get all courses for the standard of corresponding school school_name    
        courses = sub_account.get_courses()
    #get the school code and append the standard to it
    school_code = get(schooolcode) + standard
    for c in courses:
            if  school_code in c.sis_course_id:
                if not c.blueprint:
                    c.enroll_user(user_Canvas.id)
    try:
        if int(profile.standard)<10:
            std ="CL0"+profile.standard
        else:
            std = "CL"+profile.standard
        for c in courses:
            if  std in c.sis_course_id:
                if not c.blueprint:
                    c.enroll_user(user_Canvas.id)
    except Exception as e:
        print(std,e,profile.Role,c.sis_course_id,user_Canvas.id)

    
    #school_code = Schools.objects.values('school_code').filter("schoolname" = school_name) #check how to write filter
