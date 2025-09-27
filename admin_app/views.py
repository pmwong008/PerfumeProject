from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user_only
from .forms import SignUpForm
from .profiles import UserProfile
from ai_app.models import Order
from perfume_app.models import Review

from django.contrib import messages

# Create your views here.
@unauthenticated_user_only
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # 儲存User模型
            user = form.save()

            # 取出額外欄位
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')

            # 建立並儲存使用者Profile（MongoDB）
            profile = UserProfile(user_id=user.id, name=name, address=address, points=0)
            profile.save()

            # 透過 authenticate 登入
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("perfume_app:index")
            else:
                form.add_error(None, "Authentication failed after sign up. Please login manually.")
    else:
        form = SignUpForm()

    return render(request, 'admin_app/signup.html', {'form': form})


@login_required
def delete_account(request):
    user = request.user

    if request.method == "POST":

        user.delete()  # 刪除用戶資料

        messages.success(request, "Your account has been successfully deleted.")
        return redirect('perfume_app:index')  # 刪除後跳轉頁面，如首頁

    return render(request, "admin_app/delete_confirm.html")

def profile(request):

    orders = Order.objects.filter(user=request.user)

    # 取得用戶已評論的 perfume id 集合
    reviewed_perfume_ids = set(Review.objects.filter(user=request.user).values_list('perfume_id', flat=True))

    # 將 has_reviewed 屬性加到每個 order
    for order in orders:
        order.has_reviewed = order.perfume_id in reviewed_perfume_ids

    try:
        profile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user_id=request.user.id)

    if request.method == 'POST':
        # 從 POST 取得欄位
        email = request.POST.get('email')
        name = request.POST.get('name')
        address = request.POST.get('address')
        avatar = request.FILES.get('avatar')

        # 更新 Django User
        if email:
            request.user.email = email

        if avatar:
            request.user.avatar = avatar

        request.user.save()

        # 更新 MongoDB UserProfile
        if name:
            profile.name = name

        if address:
            profile.address = address

        profile.save()

        messages.success(request, 'Profile has updated already')
        return redirect('admin_app:profile')

    context = {
        'orders': orders,
        'profile':profile,
        'email': request.user.email,
        'name': profile.name if profile else '',
        'address': profile.address if profile else '',

    }
    return render(request, 'admin_app/profile.html', context)

