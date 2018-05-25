from django.shortcuts import render,redirect,HttpResponse
from . models import *
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'QuoteDashApp/index.html')

def home(request):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=request.session['ID']),
            'quotes':Quotes.objects.all()
        }
        return render(request,'QuoteDashApp/home.html',context)
    else:
        return redirect('/')

def register(request):
    if request.method=='POST':
        errors=Users.objects.registration_validator(request.POST)
                
        if len(errors):
            for key,value in errors.items():
                messages.error(request,value)
                print(key)
            return redirect('/')
        else:
            password=request.POST['txtPWord']
            pwHash=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
            print(pwHash)
            Users.objects.create(first_name=request.POST['txtFirst'],last_name=request.POST['txtLast'],email_address=request.POST['txtEmail'],password=pwHash)

            user=Users.objects.get(email_address=request.POST['txtEmail'])
            request.session['ID']=user.id

    return redirect('/home')

def login(request):
    validator=Users.objects.login_validator(request.POST)
    if 'ID' not in validator:
        for key,value in validator.items():
            messages.error(request,value)
            print(key)
        return redirect('/')
    else:    
        request.session['ID']=validator['ID']
        return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/')
    
def editUser(request,id):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=id)
        }
        return render(request,'QuoteDashApp/editUser.html',context)
    else:
        return redirect('/home')

def saveUser(request,id):
    if request.method=='POST':
        errors=Users.objects.edit_user_validator(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
                print(key)
            return redirect('/home')
        else:
            user=Users.objects.get(id=id)
            user.first_name=request.POST['txtFirst']
            user.last_name=request.POST['txtLast']
            user.email_address=request.POST['txtEmail']
            user.save()

    return redirect('/home')

def newQuote(request,id):
    if request.method=='POST':
        errors=Users.objects.post_validator(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
                print(key)
            return redirect('/home')
        else:
            user=Users.objects.get(id=id)
            Quotes.objects.create(author=request.POST['txtAuthor'],message=request.POST['txtQuote'],posted_by=user)

    return redirect('/home')

def user(request,id):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=id),
            'quotes':Quotes.objects.filter(posted_by_id=id)
        }
        return render(request,'QuoteDashApp/user.html',context)
    else:
        return redirect('/')

def like(request,id):
    if 'ID' in request.session:
        user=Users.objects.get(id=int(request.session['ID']))
        user.liked.add(Quotes.objects.get(id=id))
        return redirect('/home')
    else:
        return redirect('/')

def delete(request,qid):
    if 'ID' in request.session:
        Quotes.objects.get(id=qid).delete()
        return redirect('/home')
    else:
        return redirect('/')

