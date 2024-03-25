from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import CustomUser
import requests
from django.http import HttpResponse

def download_file(request,):
    # Fetch the file from the provided URL
    file_url = "https://docuware.fileit.org/DownloadCustomBundleFile.aspx"
    response = requests.get(file_url)
    
    # Extract the file name from the URL
    file_name = file_url.split('/')[-1]
    
    # Get the username of the user downloading the file
    username = request.user.username
    
    # Print the file name and username
    print(f"File Name: {file_name}")
    print(f"Downloading user: {username}")
    
    # Prepare the response with the fetched file content
    file_content = response.content
    content_type = response.headers.get('content-type', 'application/octet-stream')
    response = HttpResponse(file_content, content_type=content_type)
    
    # Set the content disposition to force the browser to download the file
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    # Return the response
    return response

# Create your views here.
def home(request):
    return render(request, 'user/users.html')

def getLink(request):

    return render(request, 'user/link.html')
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