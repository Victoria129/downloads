from django.shortcuts import redirect
from django.urls import reverse

def authentication_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to the login page
            return redirect(reverse('myapp:login'))  # Replace 'myapp:login' with your login URL name
    return wrapper
