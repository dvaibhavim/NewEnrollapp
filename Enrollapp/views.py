from django.shortcuts import render
from django.http import JsonResponse
from Enrollapp.forms import  UserForm,UserProfileInfoForm
from canvasapi import Canvas
from django.views.decorators.csrf import csrf_exempt
from Enrollapp.models import UserProfileInfo, Schools
from django.contrib.auth.models import User 
# Create your views here.

@csrf_exempt
def success(request):
    return render(request,'enrollapp/update_school_sucess.html')

# Create your views here.
def handle404(request, exception):
     return render(request, 'enrollapp/404.html', status=404)

#logic to create account in NagaedEd digital and enroll user to corresponsing class courses
@csrf_exempt
def create_account_NDS(request):
    if 'term' in request.GET:
        qs = Schools.objects.filter(Name__istartswith = request.GET.get('term')) #i stands for case insensitive
        school_name = list() #the url in javascript expects an json response
        for school in qs:
            school_name.append(school.Name)

        return JsonResponse(school_name, safe=False)
    elif request.method=="POST":
        registered = False
        user  = User.objects.create_user(request.POST.get("q55_emailAddress"), request.POST.get("q55_emailAddress"))
        user.set_password(user.set_unusable_password())
        user.save()      
        sis_id = UserProfileInfo.objects.order_by('sis_id').last()       
        profile = UserProfileInfo.objects.create(user = user,date_of_birth=request.POST.get("q39_birthDate39[day]")+"/"+request.POST.get("q39_birthDate39[month]")+"/"+request.POST.get("q39_birthDate39[year]"),firstname = request.POST.get("q56_name[first]"),lastname = request.POST.get("q56_name[last]"),gender = request.POST.get("Gender"),Role = request.POST.get("role"),standard = request.POST.get("class_school"),sis_id = int(sis_id.sis_id)+1, school_namme = school_name )
        profile.save()
        
        API_URL = "https://learn.nagaed.com/"
    # Canvas API key
        API_KEY = "puoPtPQS1lGkhuaPEhmTreh2MZTtj1clp4OEiZ1UVVpugZBOn76WBue5Zf3MKBl5"   

        #SIS_ID LOGIC

        # Initialize a new Canvas object
        canvas = Canvas(API_URL, API_KEY)
        if request.method=="POST":
            account = canvas.get_account(1)
            sis_user_id = int(profile.sis_id)
            #sis_user_id generation logic 
            if sis_user_id <10:
                Sis_id = 'S00000'+str(sis_user_id)
            elif sis_user_id <100:
                Sis_id = 'S0000'+str(sis_user_id)
            else:
                Sis_id = 'S000'+str(sis_user_id)

            user_Canvas = account.create_user(
                        user={
                            'name': profile.firstname + " " + profile.lastname, 
                            'skip_registration': False
                        },
                        pseudonym={                        
                            'sis_user_id': Sis_id,
                            'unique_id' :request.POST.get("q55_emailAddress"),
                            'send_confirmation':True,
                            'address':request.POST.get("q55_emailAddress")
                            },
                        communication_channel={
                            'type': 'email',
                            'skip_confirmation': False
                        }
                    )
            
            registered = True
            school_name = "NagaEd Digital School"
            sub_accounts =  account.get_subaccounts()
            for accounts in sub_accounts:
                if accounts.name.lower() == school_name.lower():
                    sub_account = accounts
           
            #logic to get all courses for the standard of corresponding school school_name    
            courses = sub_account.get_courses()
        #get the school code and append the standard to it
            standard = request.POST.get("class_school")
            standard = int(standard)

            print(sub_account, standard)
            #school_code = "CHS"
            try:
                if standard<10:
                    std ="CL0"+str(standard)
                else:
                    std = "CL"+str(standard)
                for c in courses:
                    if  std in c.sis_course_id:
                        if not c.blueprint:
                            c.enroll_user(user_Canvas.id)
            except Exception as e:
                print(e)
            
    else:
        return render(request,'enrollapp/Enroll_form_Nagaed_Digital.html')
    return render(request,'enrollapp/update_school_sucess.html',{"name":profile.firstname + " " + profile.lastname,"school":school_name})



#logic to register Naged Digital student to another school 
@csrf_exempt
def create_account_CHSS(request):
    
    if request.method=="POST":
        registered = False
        user  = User.objects.create_user(request.POST.get("q55_emailAddress"), request.POST.get("q55_emailAddress"))
        user.set_password(user.set_unusable_password())
        user.save()      
        sis_id = UserProfileInfo.objects.order_by('sis_id').last()  
        school_name = "Christian Standard Higher Secondary School"     
        profile = UserProfileInfo.objects.create(user = user,date_of_birth=request.POST.get("q39_birthDate39[day]")+"/"+request.POST.get("q39_birthDate39[month]")+"/"+request.POST.get("q39_birthDate39[year]"),firstname = request.POST.get("q56_name[first]"),lastname = request.POST.get("q56_name[last]"),gender = request.POST.get("Gender"),Role = request.POST.get("role"),standard = request.POST.get("class_school"),sis_id = int(sis_id.sis_id)+1, school_namme = school_name )
        profile.save()
        
        API_URL = "https://learn.nagaed.com/"
    # Canvas API key
        API_KEY = "puoPtPQS1lGkhuaPEhmTreh2MZTtj1clp4OEiZ1UVVpugZBOn76WBue5Zf3MKBl5"   

        #SIS_ID LOGIC

        # Initialize a new Canvas object
        canvas = Canvas(API_URL, API_KEY)
        if request.method=="POST":
            account = canvas.get_account(1)
            sis_user_id = int(profile.sis_id)
            #sis_user_id generation logic 
            if sis_user_id <10:
                Sis_id = 'S00000'+str(sis_user_id)
            elif sis_user_id <100:
                Sis_id = 'S0000'+str(sis_user_id)
            else:
                Sis_id = 'S000'+str(sis_user_id)

            user_Canvas = account.create_user(
                        user={
                            'name': profile.firstname + " " + profile.lastname, 
                            'skip_registration': False
                        },
                        pseudonym={                        
                            'sis_user_id': Sis_id,
                            'unique_id' :request.POST.get("q55_emailAddress"),
                            'send_confirmation':True,
                            'address':request.POST.get("q55_emailAddress")
                            },
                        communication_channel={
                            'type': 'email',
                            'skip_confirmation': False
                        }
                    )
            
            registered = True
            sub_accounts =  account.get_subaccounts()
            for accounts in sub_accounts:
                if accounts.name.lower() == school_name.lower():
                    sub_account = accounts
           
            #logic to get all courses for the standard of corresponding school school_name    
            courses = sub_account.get_courses()
        #get the school code and append the standard to it
            standard = request.POST.get("class_school")
            standard = int(standard)

            #school_code = "CHS"
            try:
                if standard<10:
                    std ="CL0"+str(standard)
                else:
                    std = "CL"+str(standard)
                for c in courses:
                    if  std in c.sis_course_id:
                        if not c.blueprint:
                            c.enroll_user(user_Canvas.id)
            except Exception as e:
                print(e)
            
    else:
        return render(request,'enrollapp/enroll_form.html')
    return render(request,'enrollapp/update_school_sucess.html',{"name":profile.firstname + " " + profile.lastname,"school":school_name})

       
    





"""function to create new user and send registration email. If the account gets created, course is also assigned to the student. """
@csrf_exempt
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
                        'sis_user_id': 'vd_test6',
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
            print(accounts)
            if accounts.name.lower() == school_name.lower():
                sub_account = accounts
        
        #logic to get all courses for the standard of corresponding school school_name  
        print(sub_account)
        courses = sub_account.get_courses()
    #get the school code and append the standard to it
        school_code = "CHS"
        for c in courses:
                if  school_code in c.sis_course_id:
                    if not c.blueprint:
                        c.enroll_user(user_Canvas.id)
    return render(request,'enrollapp/update_school_sucess.html')