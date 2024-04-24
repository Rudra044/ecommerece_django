from functools import wraps
from rest_framework.response import Response

def is_seller(view_func):
    @wraps(view_func)
    def decorator(self, request, *args, **kwargs):
        user = request.user
        if user:
            if user.role == 2:
                return view_func(self, request, *args, **kwargs)
            else:
                return Response({"error":"you are not authorised to access this page"})
        else:
            return Response({"error":"User not exist"})
    return decorator