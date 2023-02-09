from django.shortcuts import redirect


def allowed_role(role):
    """Role can either be 'candidate' or 'company'"""

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if (role == "candidate" and request.user.is_candidate) or (
                role == "company" and request.user.is_company
            ):
                return view_func(request, *args, **kwargs)
            else:
                return redirect("home")

        return wrapper_func

    return decorator
