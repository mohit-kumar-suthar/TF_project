from django.shortcuts import render,HttpResponse,redirect
from tf_app.form import login,register,forgot,check_password,reset_password
from django.contrib.auth.models import User
from tf_app.secure_link import encode,decode
from tf_app.send_email import send
from django.contrib.auth import authenticate,login as Login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    form = login()
    if request.method == 'POST':
        form = login(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('login successfully')
                else:
                    return HttpResponse('account disabled')
            else:
                return HttpResponse('username or password invalid')
    return render(request,'login.html',{
        'login_form':form,
    })

def register_view(request):
    form = register()
    if request.method == 'POST':
        form= register(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']        
            user = User.objects.create_user(
                username=username,
                password=form.cleaned_data['password'],
                email=email,
                is_active=False,
            )
            user.save()
            user_detail = User.objects.get(username=username)
            token = encode(email,user_detail.date_joined)
            send('register',username,email,token)
            return render(request,'register.html',{
                'register_form':register(),
                'email':email,
            })
    return render(request,'register.html',{'register_form':form})

def activate_view(request,token):
    try:
        user=decode(token,'register',True)
        form=check_password(initial={'email':user.email})
        if request.method=='POST':
            form=check_password(request.POST)
            if form.is_valid():
                user=decode(token,'register',False)
                if not user.is_active:
                    user.is_active=True
                    user.save()
                    return redirect('login')
                else:
                    return HttpResponse("invalid")
        return render(request,'email_activate.html',{
            'activate_form':form,
            'title':'Activate Account'})
    except:
        return HttpResponse('invalid')
  
def forgot_view(request):
    form= forgot()
    if request.method == 'POST':
        form = forgot(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_detail = User.objects.get(email=email)
            token = encode(email,user_detail.last_login)
            send('password',user_detail.username,email,token)
            return render(request,'email_activate.html',{
                'email':email,
                'forgot_form':form,
                'title':'Forgot Password',
            })
    return render(request,'email_activate.html',{
        'forgot_form':form,
        'title':'Forgot Password'})

def reset_password_view(request,token):
    try:
        user_true = decode(token,'password',True)
        form = reset_password(initial={'email':user_true.email})
        if request.method == 'POST':
            form = reset_password(request.POST)
            user_false = decode(token,'password',False)
            if user_false.is_active:
                if form.is_valid():
                    user_false.set_password(form.cleaned_data['password'])
                    user_false.save()
                    return redirect('login')
            else:
                return HttpResponse('invalid')
        return render(request,'email_activate.html',{
            'reset_form':form,
            'title':'Reset Password'})
    except:
        return HttpResponse(user_false)

def index_view(request):
    return render(request,'index.html')

def project_view(request):
    return render(request,'project.html')

@login_required(login_url='login')
def source_code_view(request):
    return render(request,'source_code.html')

def blog_view(request):
    return render(request,'blog.html')

@login_required(login_url='login')
def member_view(request):
    return render(request,'member.html')

def about_view(request):
    return render(request,'about.html')
