from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    ''' Redirects user to home if already logged in '''
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_groups(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.users.groups.exists():
                group = request.users.groups.all()[0].name # The first group
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                HttpResponse('Not Authorized')
        return wrapper_func
    return decorator
