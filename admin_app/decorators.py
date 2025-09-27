from django.http import HttpResponse

def unauthenticated_user_only(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("For guest only.Please logout first,if you want to signup")
        return view(request, *args, **kwargs)
    return wrapper