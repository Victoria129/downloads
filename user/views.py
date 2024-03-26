from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser,Logs
import requests
from django.http import HttpResponse
import requests
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from .forms import BootstrapAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def download_file(request):
    print("fetching this file now")
    file_url = "https://docuware.fileit.org/DownloadCustomBundleFile.aspx"
    response = requests.get(file_url)
    content_disposition_header = response.headers.get('Content-Disposition')
    if content_disposition_header:
        filename = content_disposition_header.split('=')[1].strip('"')
    else:
        filename = "downloaded_file.csv"
    print(request.user.pk)
    user = get_object_or_404(CustomUser, pk=request.user.id)
    user.filename = filename
    user.link_clicks += 1
    user.save()
    log = Logs.objects.create(user=user, filename=filename)
    file_content = response.content
    content_type = response.headers.get('Content-Type', 'application/octet-stream')
    response = HttpResponse(file_content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def home(request):
    users = CustomUser.objects.all()
    return render(request, 'user/users.html',context={"users":users})

@login_required
def getLink(request):
  

    return render(request, 'user/link.html')

@login_required
@csrf_exempt
def addUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')  
        user = CustomUser.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({'status': 'success', 'message': 'User created successfully'})
    else:
        # If the request method is not POST, return a JSON response with an error message
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def login_view(request):
    if request.method == 'POST':
        form = BootstrapAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = BootstrapAuthenticationForm()
    
    return render(request, 'user/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def delete_user(request, user_id):
    # Retrieve the user object or return 404 if not found
    user = get_object_or_404(CustomUser, pk=user_id)

    # Delete the user
    user.delete()
    users = CustomUser.objects.all()
    return redirect('users')


def make_user_superuser(request, user_id):
    try:
        user = get_object_or_404(CustomUser, pk=user_id)
        user.is_superuser = True
        user.save()
        return redirect('users')
    except user.DoesNotExist:
           return redirect('users')
    
def revoke_user_superuser(request, user_id):
    try:
        user = get_object_or_404(CustomUser, pk=user_id)
        user.is_superuser = False
        user.save()
        return redirect('users')
    except user.DoesNotExist:
           return redirect('users')
def get_logs(request):
    logs = Logs.objects.all()
    return render(request, 'user/logs.html', {'logs': logs})

def get_user_logs(request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        logs = Logs.objects.filter(user=user)
        return render(request, 'user/logsid.html', {'logs': logs,"user":user})