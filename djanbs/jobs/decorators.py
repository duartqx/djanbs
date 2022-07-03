from django.shortcuts import redirect


def allowed_groups(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name # The first group
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home')
        return wrapper_func
    return decorator
