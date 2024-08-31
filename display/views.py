from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from datetime import datetime
from .models import Member, Condition, Allergy, Medication, Aid, Dependent
import json
import requests as rq

# Create your views here.
def index(requests):
    if aut_admin(requests) == 0:
        return redirect('login')
    return render(requests, 'index.html')

def dependents(requests):
    if aut_admin(requests) == 0:
        return redirect('login')
    return render(requests, 'dependent.html')

def search(requests):
    if aut_admin(requests) == 0:
        return redirect('login')
    return render(requests, 'search.html')

def sos(requests):
    if aut_admin(requests) == 0:
        return redirect('login')
    return render(requests, 'sos.html')

def settings(requests):
    if aut_admin(requests) == 0:
        return redirect('login')
    return render(requests, 'settings.html')

def apps(requests):
    if aut_admin(requests) == 0:
        return redirect('login')
    return render(requests, 'apps.html')

def problems(requests):
    
    return render(requests, 'problems.html')

def login(requests):
    return render(requests, "login.html")

def signup(requests):
    member = requests.session.get('member', {})
    count = requests.session.get('count_signup', 0)
    member_id = Member.objects.filter(username=member['username'], password=member['password'])
    conditions_list = Condition.objects.filter(member=member_id[0].id)
    conditions = []
    for i in conditions_list:
        conditions.append(i.condition)
    allergy_list = Allergy.objects.filter(member=member_id[0].id)
    allergies = []
    for i in allergy_list:
        allergies.append(i.allergie)
    medication_list = Medication.objects.filter(member=member_id[0].id)
    medications = []
    for i in medication_list:
        medications.append(i.medication)
    
    return render(requests, "signup.html", {"member": member, 'count': count, 'conditions': conditions, 'allergies': allergies, 'medications': medications})

def aut_admin(requests):
    id = requests.session.get('member', None)
    if id is None:
        return False
    return True

def insert_member(requests):
    if requests.method == "POST":
        table = requests.POST.get('table')
        array = json.loads(requests.POST.get('array'))
        
        if table == "members":
            # TODO - Check for current members with same information
            object = Member(
                username = array[0],
                password = array[1],
                email = array[2],
                cellNr = array[3],
                title = array[4],
                fullname = array[5],
                lastname = array[6],
                idNr = array[7],
                initials = array[8],
                occupation = array[9],
                current_employer = array[10]
            )
            
            requests.session['member'] = {
                'username': object.username,
                'password': object.password,
                'email': object.email,
                'phone': object.cellNr,
                'fname': object.fullname,
                'lname': object.username,
                'id': object.idNr,
                'title': object.title,
                'initials': object.initials,
                'occupation': object.occupation,
                'employer': object.current_employer,
            }
            temp = requests.session.get('member')
            
            is_valid = True
            members = Member.objects.all()
            for i in members:
                if i.email == object.email and object.email != temp['email']:
                    return JsonResponse({"response": "This email is already in use"})
                if i.username == object.username and object.username != temp['username']:
                    return JsonResponse({"response": "This username already exists"})
                if temp['email'] == object.email and object.password != temp['password']:
                    return JsonResponse({"response": "This email or password does not match"})
                if temp['username'] == object.username and object.password != temp['password']:
                    return JsonResponse({"response": "This username or password does not match"})
            
            is_empty = all(value == "" for value in temp.values())
            
            if is_empty:
                object.save()
            else:
                Member.objects.filter(username=object.username, password=object.password, email=object.email).update(
                    cellNr = object.cellNr,
                    title = object.title,
                    fullname = object.fullname,
                    lastname = object.lastname,
                    idNr = object.idNr,
                    initials = object.initials,
                    occupation = object.occupation,
                    current_employer = object.current_employer
                )  
            requests.session['count_signup'] = 1
        return JsonResponse({"response": "Success"})
    return JsonResponse({"error": "This is crazy"}, status=400)

def check_login(requests):
    if requests.method == "POST":
        username = requests.POST.get('username')
        password = requests.POST.get('password')
        
        members = Member.objects.filter(username=username, password=password).first()
        member2 = Member.objects.filter(email=username, password=password).first()
        if members is not None:
            set_member_session(requests, members)
            return redirect('index')
        elif member2 is not None:
            set_member_session(requests, member2)
            return redirect('index')
        return redirect('login')
    
def set_member_session(requests, object):
    requests.session['member'] = {
                'username': object.username,
                'password': object.password,
                'email': object.email,
                'phone': object.cellNr,
                'fname': object.fullname,
                'lname': object.username,
                'id': object.idNr,
                'title': object.title,
                'initials': object.initials,
                'occupation': object.occupation,
                'employer': object.current_employer,
            }
    
def logout(requests):
    requests.session['member'] = None
    return redirect('index')

def add_items(requests):
    if requests.method == "POST":
        table = requests.POST.get('table')
        value = requests.POST.get('value')
        if table == "conditions":
            sesh = requests.session.get('member')
            if sesh:
                try:
                    member = Member.objects.get(username=sesh['username'], password=sesh['password'])
                    condition = Condition(
                        condition=value,
                        member=member
                    )
                    condition.save()
                    return JsonResponse({'response': "Success"})
                except Member.DoesNotExist:
                    return JsonResponse({'response': "Member not found"}, status=404)
            else:
                return JsonResponse({'response': "No session found"}, status=400)
        elif table == "allergies":
            sesh = requests.session.get('member')
            if sesh:
                try:
                    member = Member.objects.get(username=sesh['username'], password=sesh['password'])
                    condition = Allergy(
                        allergie=value,
                        member=member
                    )
                    condition.save()
                    return JsonResponse({'response': "Success"})
                except Member.DoesNotExist:
                    return JsonResponse({'response': "Member not found"}, status=404)
            else:
                return JsonResponse({'response': "No session found"}, status=400)
        elif table == "medicine":
            sesh = requests.session.get('member')
            if sesh:
                try:
                    member = Member.objects.get(username=sesh['username'], password=sesh['password'])
                    condition = Medication(
                        medication=value,
                        member=member
                    )
                    condition.save()
                    return JsonResponse({'response': "Success"})
                except Member.DoesNotExist:
                    return JsonResponse({'response': "Member not found"}, status=404)
            else:
                return JsonResponse({'response': "No session found"}, status=400)
        else:
            return JsonResponse({'response': "Error"})
    return JsonResponse({'response': "Error"})


def sos_request(requests):
    if requests.method == "POST":
        status = requests.POST.get("value")
    # TODO - Make entry to the database
    
    return JsonResponse({'response': "Success"})

def chatbot(request):
    return render(request, 'chatbot.html')

def askbot(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        api_key = 'sk-None-y86ZaqfDBoSsXixM1aAtT3BlbkFJ1LFmrkKOdL8qF6cscMjO'  # Replace with your actual API key
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": question}]
        }

        try:
            response = rq.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                data=json.dumps(data)
            )
            response.raise_for_status()  # Raise an error for bad status codes
            result = response.json()
            
            # Check if the expected key exists in the response
            if 'choices' in result and len(result['choices']) > 0:
                answer = result['choices'][0]['message']['content']
                return JsonResponse({'answer': answer})
            else:
                return JsonResponse({'error': 'Unexpected API response format'}, status=500)
        
        except rq.exceptions.RequestException as e:
            # Log the error or handle it appropriately
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)