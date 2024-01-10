from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Contact
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.
# def connect_db(collection_name):
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = client["xenonstack"]
#     return db[collection_name]

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         db = connect_db('users')
#         user_check = db.find_one({'username': username})
#
#         if user_check is None:
#             return render(request, "login.html", {'mssg': True, 'mssgTxt': "Username doesn't exists!!"})
#
#         else:
#             if password != user_check['password']:
#                 return render(request, "login.html", {'mssg': True, 'mssgTxt': "Type the correct Password!!"})
#
#             else:
#                 auth.login(request,username)
#                 redirect('/theme')
#
#     return render(request, "login.html")

# def signup(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         username = request.POST.get('name')
#         password = request.POST.get('password')
#         repassword = request.POST.get('repassword')
#
#         if password != repassword:
#             return render(request, "signup.html",{"mssg":True, "mssgTxt": "Password are not same!"})
#
#         db = connect_db('users')
#         user_check = db.find_one({'username': username})
#
#         if user_check:
#             return render(request, "signup.html", {"mssg": True, "mssgTxt": "Username Already exists"})
#
#         else:
#             db.insert_one({"name":name, "username": username, "password": password})
#
#     return render(request, "signup.html")

@login_required(login_url='/')
def theme(request):
    if request.method == "POST":
        auth.logout(request)
        return render(request, 'login.html')
    return render(request, 'main_page.html')

@login_required(login_url='/contact')
def contact(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        phn = request.POST.get('phn')

        if name and email and phn:
            contact = Contact.objects.create(name=name,phone_number=phn,email=email)
            contact.save()
            return render(request, 'contact.html', {"mssg": True, "mssgTxt": "Contact Details are saved!"})
        else:
            return render(request, 'contact.html', {"mssg": True, "mssgTxt": "Some Details are missing!"})
    return render(request, 'contact.html')

def login(request):
    auth.logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user_check = auth.authenticate(username=username, password=password)
            if user_check:
                auth.login(request, user_check)
                return redirect('/contact')
            else:
                return render(request, "login.html", {'mssg': True, 'mssgTxt': "Username doesn't exists!!"})
        else:
            return render(request, "login.html", {'mssg': True, 'mssgTxt': "Some Details are missing!!"})
    return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if username and password and repassword:
            if password != repassword:
                return render(request, 'signup.html', {"mssg": True, "mssgTxt": "Paswword doesn't match!"})
            else:
                if not User.objects.filter(username=username).exists():
                    if len(password) < 6:
                        return render(request, 'signup.html', {"mssg": True, "mssgTxt": "Password Too Short"})

                    else:
                        user = User.objects.create_user(username=username)
                        user.set_password(password)
                        user.is_active = True
                        user.save()
                        return render(request, 'signup.html',
                                      {"mssg": True, "mssgTxt": "User has been Created, Click on the Already user!!"})
                else:
                    return render(request, 'signup.html', {"mssg": True, "mssgTxt": "User already Exists!!"})
        else:
            return render(request, "login.html", {'mssg': True, 'mssgTxt': "Some Details are missing!!"})
    return render(request,'signup.html')