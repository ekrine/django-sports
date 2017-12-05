from .models import User
from rest_framework import status
from rest_framework.response import Response

# def shortcircuitmiddleware(f):
#     def _shortcircuitmiddleware(*args, **kwargs):
#         return f(*args, **kwargs)
#     return _shortcircuitmiddleware
#
# class ShortCircuitMiddleware(object):
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         return self.get_response(request)
#
#     def process_exception(self, request, exception):
#         print exception.__class__.__name__
#         print exception.message
#         return None
#
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         if view_func.func_name == "_shortcircuitmiddleware":
#             print "haha"
#             return view_func(request, *view_args, **view_kwargs)
#         print view_func.func_name
#         print "Not here"
#         return None

class SimpleMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            User.objects.get(id=view_args[0].data.get('userId'))
            return view_func(request, *view_args, **view_kwargs)
        except:
            return Response({"message": "Invalid authentication"},
                            status.HTTP_401_UNAUTHORIZED,
                            content_type="application/json")