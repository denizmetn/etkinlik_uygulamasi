from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, "Bu sayfaya erişmek için giriş yapmalısınız.")
                return redirect(reverse_lazy('account:login'))
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Bu sayfaya erişim yetkiniz yok.")
                # return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")
                return redirect(reverse_lazy('event:activity_list')) # Yetkisizse etkinlik listesine yönlendir
        return wrap
    return decorator