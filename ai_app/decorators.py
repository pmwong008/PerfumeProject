from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from functools import wraps
from admin_app.profiles import UserProfile
from django.contrib import messages
from .models import Order

def status_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects(user_id=user.id).first()
        if profile and profile.status:
            return view_func(request, *args, **kwargs)
        else:
            # 如果status是False，重定向或錯誤頁
            messages.warning(request, "Please comment the perfume,before get sample again")
            return redirect('/profile/')  # 自行設定
    return _wrapped_view

def sample_order_check(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        perfume_id = request.GET.get('perfume_id') or kwargs.get('perfume_id')
        if not perfume_id:
            messages.error(request, "Missing perfume_id.")
            return render(request, 'error_page.html')

        has_ordered = Order.objects.filter(user=user, perfume_id=perfume_id).exists()
        if has_ordered:
            messages.warning(request, "Sample has sent already, please choose another perfume.")
            # 重導回香水列表頁，可改成合適頁面,可加其他要帶的 context
            return redirect('/perfumes_list/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view



