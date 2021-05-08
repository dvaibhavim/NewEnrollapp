from django.shortcuts import render
from django.http import JsonResponse
from Enrollapp.forms import  UserForm,UserProfileInfoForm
from canvasapi import Canvas
from django.views.decorators.csrf import csrf_exempt
from Enrollapp.models import UserProfileInfo, Schools
from django.contrib.auth.models import User 



import os
# Create your views here.

@csrf_exempt
def success(request):
    return render(request,'enrollapp/update_school_sucess.html')

# Create your views here.
def handle404(request, exception):
     return render(request, 'enrollapp/404.html', status=404)


def get_schoolName(request):
    """returns the list of school name typed in input field."""
    qs = Schools.objects.filter(Name__icontains = request.GET.get('term')) #i stands for case insensitive
    school_name = list() #the url in javascript expects an json response
    for school in qs:
        school_name.append(school.Name)

    return JsonResponse(school_name, safe=False)

#logic to create account in NagaedEd digital and enroll user to corresponsing class courses
@csrf_exempt
def create_account_NDS(request):
    print("in create account")
    try:
        if 'term' in request.GET:
            return get_schoolName(request)            
        elif request.method=="POST":
            registered = False
            #user  = User.objects.create_user(username=request.POST.get("q55_emailAddress"), email=request.POST.get("q55_emailAddress"),password=user.set_unusable_password())    
          
            user  = User.objects.create_user(username=request.POST.get("q55_emailAddress"), email=request.POST.get("q55_emailAddress"))    
            #user.set_password(set_unusable_password())
            try:
                sis_id = UserProfileInfo.objects.order_by('sis_id').last()
                profile = UserProfileInfo.objects.create(user = user,date_of_birth=request.POST.get("q39_birthDate39[day]")+"/"+request.POST.get("q39_birthDate39[month]")+"/"+request.POST.get("q39_birthDate39[year]"),firstname = request.POST.get("q56_name[first]"),lastname = request.POST.get("q56_name[last]"),gender = request.POST.get("Gender"),Role = request.POST.get("role"),standard = request.POST.get("class_school"),sis_id = int(sis_id.sis_id)+1)
    
            except AttributeError:
                sis_id = 1
                profile = UserProfileInfo.objects.create(user = user,date_of_birth=request.POST.get("q39_birthDate39[day]")+"/"+request.POST.get("q39_birthDate39[month]")+"/"+request.POST.get("q39_birthDate39[year]"),firstname = request.POST.get("q56_name[first]"),lastname = request.POST.get("q56_name[last]"),gender = request.POST.get("Gender"),Role = request.POST.get("role"),standard = request.POST.get("class_school"),sis_id = 1)
                         
           
            
            API_URL = "https://learn.nagaed.com/"
        # Canvas API key
            API_KEY = "puoPtPQS1lGkhuaPEhmTreh2MZTtj1clp4OEiZ1UVVpugZBOn76WBue5Zf3MKBl5"    
            # Initialize a new Canvas object
            canvas = Canvas(API_URL, API_KEY)
            if request.method=="POST":
                account = canvas.get_account(1)
                #sis_user_id generation logic 
                
                #print(sis_id,sis_id.sis_id)
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
                                'name': profile.firstname + " " + profile.lastname, # profile.firstname + " " + profile.lastname,
                                'skip_registration': False
                            },
                            pseudonym={                        
                                'sis_user_id': Sis_id,
                                'unique_id' :user.username,
                                'send_confirmation':True,
                                'address':user.username
                                },
                            communication_channel={
                                'type': 'email',
                                'skip_confirmation': False
                            }
                        )
                user.save()   
                profile.save()
                registered = True
                            #remove the school name and set the sisid of the school or account number here
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
            print("in else")
            return render(request,'enrollapp/Enroll_form_Nagaed_Digital.html')
        print("in outside")
        return render(request,'enrollapp/update_school_sucess.html',{"name":user.username,"school":school_name})
    except Exception as e:
        if "UNIQUE" in str(e) or "ID already in use" in str(e):
            msg = "User Already exists. Please Login to enroll."
        else:
            msg = str(e)
        return render(request,'enrollapp/error_page.html',{"name": msg})

#logic to register Naged Digital student to another school 
@csrf_exempt
def create_account_CHSS(request):
    try:
        from canvasapi import Canvas
        API_URL = "https://learn.nagaed.com/"
        # Canvas API key
        API_KEY = "puoPtPQS1lGkhuaPEhmTreh2MZTtj1clp4OEiZ1UVVpugZBOn76WBue5Zf3MKBl5"    
            #SIS_ID LOGIC
    
            # Initialize a new Canvas object
        canvas = Canvas(API_URL, API_KEY)
        if request.method=="POST":
            registered = False
            user  = User.objects.create_user(request.POST.get("q55_emailAddress"), request.POST.get("q55_emailAddress"))
            user.set_password(user.set_unusable_password())
            user.save()      
            sis_id = UserProfileInfo.objects.order_by('sis_id').last()  
            #remove the school name and set the sisid of the school or account number here
            school_name = "Christian Standard Higher Secondary School"     
            profile = UserProfileInfo.objects.create(user = user,date_of_birth=request.POST.get("q39_birthDate39[day]")+"/"+request.POST.get("q39_birthDate39[month]")+"/"+request.POST.get("q39_birthDate39[year]"),firstname = request.POST.get("q56_name[first]"),lastname = request.POST.get("q56_name[last]"),gender = request.POST.get("Gender"),Role = request.POST.get("role"),standard = request.POST.get("class_school"),sis_id = int(sis_id.sis_id)+1 )
            profile.save()
            
           
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
        return render(request,'enrollapp/update_school_sucess.html',{"name":user.username,"school":school_name})
    except Exception as e:
        if "UNIQUE" in str(e) or "ID already in use" in str(e):
            from canvasapi import Canvas
            
            API_URL = "https://learn.nagaed.com/"
            API_KEY = "puoPtPQS1lGkhuaPEhmTreh2MZTtj1clp4OEiZ1UVVpugZBOn76WBue5Zf3MKBl5"
            canvas = Canvas(API_URL, API_KEY)
            
            account = canvas.get_account(1)
            user_c = account.get_users()
            email = request.POST.get("q55_emailAddress")
            for u in user_c:
                if u.login_id==email:
                    u = u.id
                    break
            
            school_name = "Christian Standard Higher Secondary School"  
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
            if standard<10:
                std ="CL0"+str(standard)
            else:
                std = "CL"+str(standard)
            for c in courses:
                if  std in c.sis_course_id:
                    if not c.blueprint:
                        c.enroll_user(u)
            return render(request,'enrollapp/update_school_sucess.html',{"name":email,"school":school_name})
        else:
            msg = str(e)
            return render(request,'enrollapp/error_page.html',{"name": msg})


#verify the user's email address.
#def verify_email(request):
"""
 First check if the user is registered, if not send error user not registered else send email verification email with link to update school.
"""

#logic to register Naged Digital student to another school 
@csrf_exempt
def register(request):
    #user_form = UserForm()
    profile_form = UserProfileInfoForm()
    #code for autocomplete search used to fetch school name from database
    if 'term' in request.GET:
        return get_schoolName(request)
    elif request.method == "POST":
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
                            'sis_user_id': 'vd_test1',
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
                if accounts.name.lower() == school_name.lower():
                    sub_account = accounts
            
            #logic to get all courses for the standard of corresponding school school_name    
            courses = sub_account.get_courses()
        #get the school code and append the standard to it
            school_code = "CHS"
            for c in courses:
                    if  school_code in c.sis_course_id:
                        if not c.blueprint:
                            c.enroll_user(user_Canvas.id)
    else:
        return render(request,'enrollapp/Enroll_form_Nagaed_Digital.html')
    return render(request,'enrollapp/update_school_success.html')

       
    





"""function to create new user and send registration email. If the account gets created, course is also assigned to the student. """
@csrf_exempt
def old_user_update(request):
    try:
        if 'term' in request.GET:
           return get_schoolName(request)
        elif request.method=="POST":  
            email = request.POST.get("q55_emailAddress") 
            djemail.send_email(
                to=email,
                template_name="enrollapp/verify.txt", # .txt and/or .html  ,
                context={'variable': 'Variable Content'},
                subject="Complete Verification Process for updating school in NagaEd."
            )
        else:
            return render(request,os.path.join("enrollapp","Old_user.html"))
    except Exception as e:
        return render(request,'enrollapp/error_page.html',{"name": str(e)})
        
