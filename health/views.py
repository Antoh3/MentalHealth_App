from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import Patient,Counselor,Message,Session,Post
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
import time
import random
from datetime import datetime


last_message_id = None

def chatbot_redirect(request):
    return redirect("http://localhost:8501") 

@csrf_exempt
def get_messages(request, user_type, user_id):
    if request.method == "GET":
        try:
            messages = Message.objects.filter(
                receiver_patient_id=user_id if user_type == "patient" else None,
                receiver_counselor_id=user_id if user_type == "counselor" else None
            ).order_by("timestamp")

            messages_data = [
                {
                    "id": msg.id,
                    "sender": msg.sender_patient.id if msg.sender_patient else msg.sender_counselor.id,
                    "content": msg.content,
                    "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for msg in messages
            ]

            return JsonResponse({"messages": messages_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            sender_id = data["sender_id"]
            receiver_id = data["receiver_id"]
            sender_type = data["sender_type"]
            content = data["content"]

            print(data)

            sender_model = Patient if sender_type == "patient" else Counselor
            receiver_model = Counselor if sender_type == "counselor" else Patient
            print("sender model",sender_model)
            print("center",receiver_model)
            sender = get_object_or_404(sender_model, id=sender_id)
            # print("center1",sender)
            receiver = get_object_or_404(receiver_model, id=receiver_id)
            # print("receiver",receiver)

            # print("sender",sender,"receiver",receiver)

            message = Message.objects.create(
                sender_patient=sender if sender_type == "patient" else None,
                sender_counselor=sender if sender_type == "counselor" else None,
                receiver_patient=receiver if sender_type == "patient" else None,
                receiver_counselor=receiver if sender_type == "counselor" else None,
                content=content,
                timestamp=timezone.now()
            )

            return JsonResponse({"success": True, "message_id": message.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": "errromin sending messages"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=404)

@csrf_exempt
def long_poll_messages(request, user_type, user_id):
    if request.method == "GET":
        try:
            timeout = 30
            start_time = time.time()
            last_message = Message.objects.order_by("-timestamp").first()
            last_message_id = last_message.id if last_message else 0

            while time.time() - start_time < timeout:
                messages = Message.objects.filter(
                    receiver_patient_id=user_id if user_type == "patient" else None,
                    receiver_counselor_id=user_id if user_type == "counselor" else None
                ).order_by("timestamp")

                if messages and messages.last().id > last_message_id:
                    last_message_id = messages.last().id
                    messages_data = [
                        {
                            "sender": msg.sender_patient.id if msg.sender_patient else msg.sender_counselor.id,
                            "content": msg.content,
                            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        for msg in messages
                    ]
                    return JsonResponse({"messages": messages_data})

                time.sleep(2)

            return JsonResponse({"messages": []})  

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

def chat_page(request, user_type, user_id, receiver_id):
    receiver = get_object_or_404(Patient if user_type == "counselor" else Counselor, id=receiver_id)
    messages = Message.objects.filter(
        receiver_patient_id=user_id if user_type == "patient" else None,
        receiver_counselor_id=user_id if user_type == "counselor" else None
    ).order_by("timestamp")

    return render(request, "health/chat.html", {
        "user_id": user_id,
        "user_type": user_type,
        "receiver_id": receiver_id,
        "receiver_name": receiver.first_name,
        "messages": messages
    })

def patient_redirect_home(request):
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            patient = Patient.objects.get(email = email)

            if check_password(password, patient.password):
                request.session['patient_id'] = patient.id
                messages.success(request,"login success")
                return redirect('/')
            else:
                messages.error(request,"Wrong email or password")
        except Patient.DoesNotExist:
            messages.error(request,"User not found")
    return render(request,'auth/login.html')

def patient_signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        date_of_birth = request.POST.get("date_of_birth")
        password = request.POST.get("password")
    
        if Patient.objects.filter(email = email).exists():
            messages.error(request,"User already exists")
            return render(request, 'auth/patient_signup.html')
        
        hashed_password = make_password(password)
        
        patient = Patient.objects.create(
            first_name=first_name,
            last_name = last_name,
            email=email,
            date_of_birth = date_of_birth,
            phone_number = phone_number,
            password = hashed_password
            )
        patient.save()
        messages.success(request,"Account created successfully")
        return HttpResponseRedirect(reverse("health:login"))
        
    return render(request,'auth/patient_signup.html')

def counselor_signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        specialization = request.POST.get('specialization')
        phone_number = request.POST.get('phone_number')
        license_number = request.POST.get('license_number')
        password = request.POST.get('password')

        if Counselor.objects.filter(email = email).exists():
            messages.error(request,"Email already exists")
            return render(request, 'auth/counselor_signup.html')
        
        hashed_password = make_password(password)
        counselor = Counselor.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            specialization = specialization,
            phone_number = phone_number,
            license_number = license_number,
            password = hashed_password
        )
        counselor.save()
        messages.success(request,"Account created")
        return HttpResponseRedirect(reverse("health:counselor_login"))
    return render(request, 'auth/counselor_signup.html')

def counselor_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            counselor = Counselor.objects.get(email = email)

            if check_password(password, counselor.password):
                request.session['counselor_id'] = counselor.id
                messages.success(request,"login success")
                return redirect('health:counselor_home')
            else:
                messages.error(request,"Wrong email or password")
        except Counselor.DoesNotExist:
            messages.error(request,"User not found")
    return render(request, 'auth/counselor_l.html')

def book_session(request):
    counselors = Counselor.objects.all()

    if request.method == 'POST':
        patient_id = request.session.get('patient_id')
        session_number = random.randint(100000000, 999999999)
        counselor_id = request.POST.get('counselor_id')
        content = request.POST.get('content')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        session_time = request.POST.get('session_time')
        session_date = request.POST.get('session_date')

        counselor = Counselor.objects.get(id=counselor_id)
        # print("counselor",counselor)
        patient = get_object_or_404(Patient,id=patient_id)
        if not patient:
            messages.error(request,"You should be logged first to book an appointment")
            redirect('login')

        try:
            appointment_date = datetime.strptime(session_date, '%Y-%m-%d').date()
            today_date = datetime.now().date()

            if appointment_date < today_date:
                messages.error(request, "Please select a date in the future for your appointment")
                # return redirect('appointment')
        except ValueError:
            messages.error(request,"Invalid date format")
        
        session = Session.objects.create(
            fullname = fullname,
            email = email,
            phonenumber = phonenumber,
            session_number = session_number,
            counselor_id = counselor,
            content = content,
            session_date = session_date,
            session_time = session_time,
            patient_id = patient,
        )

        messages.success(request,"Your request has been received successfully")
        return redirect('health:all_patient_sessions')


    context = {
        "counselors":counselors
    }
    return render(request,'patient/book_session.html',context)

def counselor_chat_page(request, user_type, user_id, receiver_id):
    receiver = get_object_or_404(Patient if user_type == "counselor" else Counselor, id=receiver_id)
    messages = Message.objects.filter(
        receiver_patient_id=user_id if user_type == "patient" else None,
        receiver_counselor_id=user_id if user_type == "counselor" else None
    ).order_by("timestamp")

    return render(request, "health/chat.html", {
        "user_id": user_id,
        "user_type": user_type,
        "receiver_id": receiver_id,
        "receiver_name": receiver.first_name,
        "messages": messages
    })

def home_view(request):
    patient_id = request.session.get('patient_id')
    patient = Patient.objects.filter(id = patient_id)
    
    context = {
        'patient':patient
    }
    return render(request,'index.html',context)

def test(request):
    if request.method == "POST":
        return HttpResponse("Test api")

def comm_view(request):
    patient_id = request.session.get('patient_id')
    patient = Patient.objects.filter(id = patient_id)
    post = Post.objects.all()
    
    if request.method == "POST":
        patient_id = request.session.get('patient_id')
        title = request.POST['title']
        profile_picture = request.FILES.get('profile_picture')
        profile_icon = request.FILES.get('profile_icon')
        content = request.POST['content']
        # author = request.POST['author']
        

        patientdata = get_object_or_404(Patient,id=patient_id)

        

        post = Post.objects.create(
            title = title,
            content = content,
            author = patientdata,
            profile_picture = profile_picture,
            profile_icon = profile_icon,
        )

        # context = {
        #     "user":patient,
        # }

        post.save()
        messages.success(request,"Post created successfully")
        return redirect('health:comm')

    context = {
        "posts":post,
        "user":patient,
    }
    return render(request,'health/community.html',context)

def videos_view(request):
    counselors = Counselor.objects.all()

    context = {
        "counselors":counselors
    }
    return render(request,'health/videos.html',context)

def books_view(request):
    return render(request,'books/book.html')


def counselor_home(request):
    counselor_id = request.session.get('counselor_id')
    allsessions = Session.objects.all().count()
    newsession = Session.objects.filter(status = 0).count()
    approvedsession = Session.objects.filter(status = "approved").count()
    cancelledsessions = Session.objects.filter(status = "cancelled").count()
    completedsessions = Session.objects.filter(status = 'completed').count()
    counselor = Counselor.objects.filter(id = counselor_id) 

    context = {
        "allsessions":allsessions,
        "newsession":newsession,
        "approvedsession":approvedsession,
        "cancelledsessions":cancelledsessions,
        "completedsessions":completedsessions,
        "counselor":counselor
    }

    return render(request,'counselor/counselor_home.html',context)

def patient_list(request):
    counselor_id = request.session.get('counselor_id')
    counselor = get_object_or_404(Counselor,id=counselor_id)
    patient = Session.objects.filter(status = "approved",counselor_id=counselor)

    context = {
        "patients":patient
    }
    return render(request,'counselor/patient_list.html',context)

def session_details(request,id):
    session_data = Session.objects.filter(id = id)

    context = {
        "sessions":session_data
    }
    return render(request,'counselor/session_details.html',context)

def recommenduser(request,id):
    session_data = Session.objects.filter(id = id)
    if request.method == 'POST':
        reccomendation = request.POST['reccomendation']
        status = request.POST['status']

        session = Session.objects.get(id=id)
        session.status = status
        session.reccomendation = reccomendation

        session.save()
        return redirect('health:view_session')

    context = {
        "sessions":session_data
    }

    return render(request,'counselor/recommend_session.html',context)

def view_session(request):
    session_data = Session.objects.all()

    context = {
        "sessions":session_data
    }
    return render(request,'counselor/view_session.html',context)

def patient_appintment_remark(request,id):
    if request.method == 'POST':
        remark = request.POST['remark']
        status = request.POST['status']

        session = Session.objects.get(id=id)
        session.status = status
        session.remark = remark

        session.save()
        return redirect('health:view_session')
    return render(request,'counselor/patient_new_session.html')

def all_sessions_data(request):
    counselor_id = request.session.get('counselor_id')
    counselor = get_object_or_404(Counselor,id=counselor_id)
    session = Session.objects.filter(counselor_id = counselor)

    context = {
        "sessions":session
    }
    return render(request,'counselor/all_sessions.html',context)

def all_patient_session_data(request):
    patient_id = request.session.get('patient_id')
    patient = get_object_or_404(Patient,id=patient_id)
    session = Session.objects.filter(patient_id = patient)

    context = {
        "sessions":session
    }
    return render(request,'patient/all_sessions.html',context)


def completed_sessions(request):
    counselor_id = request.session.get('counselor_id')
    counselor = get_object_or_404(Counselor,id=counselor_id)
    session = Session.objects.filter(status="completed",counselor_id = counselor)

    context = {
        "sessions":session
    }
    return render(request,'counselor/all_sessions.html',context)

def canceled_sessions(request):
    counselor_id = request.session.get('counselor_id')
    counselor = get_object_or_404(Counselor,id=counselor_id)
    session = Session.objects.filter(status="cancelled",counselor_id = counselor)

    context = {
        "sessions":session
    }
    return render(request,'counselor/all_sessions.html',context)

def approved_sessions(request):
    counselor_id = request.session.get('counselor_id')
    counselor = get_object_or_404(Counselor,id=counselor_id)
    session = Session.objects.filter(status="approved",counselor_id = counselor)

    context = {
        "sessions":session
    }
    return render(request,'counselor/all_sessions.html',context)

def new_session(request):
    counselor_id = request.session.get('counselor_id')
    counselor = get_object_or_404(Counselor,id=counselor_id)

    session = Session.objects.filter(status = '0',counselor_id=counselor)

    context = {
        "sessions":session
    }
    return render(request,'counselor/patient_new_session.html',context)

def user_search_sessions(request):
    counselor_id = request.session.get('counselor_id')
    counselor = get_object_or_404(Counselor,id=counselor_id)
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Session.objects.filter(
                fullname__icontains=query) | Session.objects.filter(
                    session_number__icontains=query) & Session.objects.filter(counselor_id = counselor)
            messages.info(request, "Searched against " + query)
            context = {
                'patient': patient, 
                'query': query, 
                }
            return render(request, 'counselor/search_session.html', context)
        else:
            print("No Record Found")
            return render(request, 'counselor/search_session.html')
    
    # If the request method is not GET
    return render(request, 'counselor/search_session.html')

def profile(request):
    counselor_id = request.session.get('counselor_id')
    counselor = Counselor.objects.filter(id=counselor_id)

    # print(counselor)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        specialization = request.POST['specialization']
        license_number = request.POST['license_number']

        counselor1 = Counselor.objects.get(id = counselor_id) 
        counselor1.first_name = first_name
        counselor1.last_name = last_name
        counselor1.email = email
        counselor1.phone_number = phone_number
        counselor1.specialization = specialization
        counselor1.license_number = license_number

        counselor1.save()
        messages.success(request,"Profile updated")
        return redirect('health:profile')

    context = {
        "user":counselor
    }
    return render(request,'counselor/profile.html',context)

def patient_search_sessions(request):
    patient_id = request.session.get('patient_id')
    user = get_object_or_404(Patient,id=patient_id)
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Session.objects.filter(
                fullname__icontains=query) | Session.objects.filter(
                    session_number__icontains=query) & Session.objects.filter(patient_id = user)
            messages.info(request, "Searched against " + query)
            context = {
                'patient': patient, 
                'query': query, 
                }
            return render(request, 'patient/search_session.html', context)
        else:
            print("No Record Found")
            return render(request, 'patient/search_session.html')
    
    # If the request method is not GET
    return render(request, 'patient/search_session.html')

def patient_session_details(request,id):
    session_data = Session.objects.filter(id = id)

    context = {
        "sessions":session_data
    }
    return render(request,'patient/session_details.html',context)
    
def counselor_chat_view(request, sender_type, sender_id, receiver_id):
    """Render the chat template with sender and receiver info."""
    return render(request, "health/counselor_chat.html", {
        "sender_type": sender_type,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
    })

def chat_view(request, sender_type, sender_id, receiver_id):
    """Render the chat template with sender and receiver info."""
    return render(request, "health/chat.html", {
        "sender_type": sender_type,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
    })

def test(request):
    return render(request,'auth/login.html')


def videoCall(request,session_id):
    session = Session.objects.get(id=session_id)

    counselor_phone = session.counselor_id.phone_number

    context = {
        "session":session,
        "counselor_phone_number":counselor_phone
    }
    return render(request,'health/videocall.html',context)