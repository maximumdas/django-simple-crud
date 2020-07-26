# from django.shortcuts import render
# from django.http import HttpResponse, HttpResponseRedirect
# from .models import User
# from .forms import RegisterUser

# Create your views here.

# def index(response):
#     user = User.objects.all()
#     return render(response, "register/users.html", {"user": user})

# def register(response):
#     if response.method == 'POST':
#         form = RegisterUser(response.POST)

#         if form.is_valid():
#             # Buat objek baru disini
#             # newEmail = form.cleaned_data["email"]
#             # newName = form.cleaned_data["name"]
#             # newPassword = form.cleaned_data["password"]
#             form.save()
#             # newUser = User(email = newEmail, name = newName, password = newPassword)
#             # newUser.save()

#             return HttpResponseRedirect('/login/')
#     else:
#         form = RegisterUser()
#     return render(response, "register/register.html", {"form": form})

# def login(response):
#     return render(response, "register/login.html", {})

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import AppUsers
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.http import QueryDict
import json

class OrderListJson(BaseDatatableView):
    # The model we're going to show
    model = AppUsers

    # define the columns that will be returned
    columns = ['name', 'email', 'profil_url', 'id']

    order_columns = ['name', 'email', '', '']

    visible_columns = ['name', 'email', 'profil_url', '']

    max_display_length = 10

    def render_column(self, row, column):
        if column == 'profil_url':
            return "<img src='"+row.profil_url.url+"' style='width:200px; height:200px'>"
        else:
            return super(OrderListJson, self).render_column(row, column)

@csrf_exempt
def index(request):
    id = request.session.get('id', None)
    if id:
        return redirect('/users')
    else:
        return render(request, 'register/regist.html',{'is_login':id})

@csrf_exempt
def register(request):
    id = request.session.get('id', None)
    if id:
        return redirect('/users')
    else:
        if request.method == 'POST' and request.FILES['profil_url']:
            myfile = request.FILES['profil_url']
            # fs = FileSystemStorage(location='./media/photos/')
            # filename = fs.save(myfile.name, myfile)
            # uploaded_file_url = fs.url(filename)

            errors = AppUsers.objects.validator(request.POST)
            if len(errors):
                for tag, error in errors.items():
                    
                    messages.error(request, error, extra_tags=tag)
                return JsonResponse(errors, status=500)

            hashed_password = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
            user = AppUsers.objects.create(name=request.POST['name'], email=request.POST['email'], password=hashed_password.decode('utf-8'), profil_url=myfile)
            user.save()
            request.session['id'] = user.id
        return JsonResponse({'message': 'Berhasil menambah akun'})
    
@csrf_exempt
def login(request):
    id = request.session.get('id', None)
    if id:
        return redirect('/users')
    else:
        if request.method == 'POST':
            try:
                user = AppUsers.objects.filter(email=request.POST['email'])
            except:
                return JsonResponse({'messages': 'Email tidak dikenali'}, status=401)
            if (bcrypt.checkpw(request.POST['password'].encode('utf-8'), user[0].password.encode('utf-8'))):
                request.session['id'] = user[0].id
                user.update(is_login=True)
                return JsonResponse({'messages': 'Berhasil login'})
            else:
                return JsonResponse({'messages': 'Password salah'}, status=401)
        else:
            return render(request, 'register/login.html',{'is_login':id})

@csrf_exempt
def delete(request):
    id = request.session.get('id', None)
    if id:
        payload = json.loads(request.body)
        print(payload['email'])
        AppUsers.objects.get(email=payload['email']).delete()
        return JsonResponse({'messages': 'User dihapus!'})
    else:
        return redirect('/login')

@csrf_exempt
def userList(request):
    id = request.session.get('id', None)
    if id:
        return render(request, 'register/users.html', {'is_login':id})
    else:
        return redirect('/login')

@csrf_exempt
def updateUser(request):
    id = request.session.get('id', None)
    if id:
        if (request.POST['part'] == 'bio'):
            user = AppUsers.objects.filter(id=request.POST['id'])
            files = request.FILES.get('profil_url', None)
            if files:
                user.update(name=request.POST['name'], email=request.POST['email'])
                user2 = AppUsers.objects.get(id=request.POST['id'])
                user2.profil_url = request.FILES['profil_url']
                user2.save()
            else:
                user.update(name=request.POST['name'], email=request.POST['email'])
            return JsonResponse({'messages': 'Berhasil merubah biodata!'})
        else:
            user = AppUsers.objects.filter(id=request.POST['id'])
            hashed_password = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
            user.update(password=hashed_password.decode('utf-8'))
            return JsonResponse({'messages': 'Berhasil merubah password!'})
    else:
        return redirect('/login')

@csrf_exempt
def logout(request):
    id = request.session.get('id', None)
    if id:
        user = AppUsers.objects.get(id=id)
        user.is_login = False
        user.save()
        request.session['id'] = None
    return JsonResponse({'messages': 'Logout!'})