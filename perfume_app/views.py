from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render,redirect
from django.core.paginator import Paginator
from django.db.models import Q
from perfume_app.models import Perfumes,Review
from ai_app.models import Order
from admin_app.profiles import UserProfile

import json
from django.db.models import Avg

# Create your views here.
def index(request):

    return render(request,'perfume_app/index.html')

def user_guide(request):

    return render(request, 'perfume_app/user_guide.html')

def extract_notes(notes_str):
    notes_set = set()
    try:
        notes_data = json.loads(notes_str)
        if isinstance(notes_data, dict):
            for val in notes_data.values():
                if isinstance(val, list):
                    notes_set.update(str(n) for n in val if n is not None)
                else:
                    if val is not None:
                        notes_set.add(str(val))
        elif isinstance(notes_data, list):
            notes_set.update(str(n) for n in notes_data if n is not None)
        # elif notes_data is not None:
        #     notes_set.add(str(notes_data))
    except Exception:
        if notes_str:
            notes_set.add(str(notes_str))
    return notes_set

def perfumes_list(request):
    all_brands = Perfumes.objects.values_list('brand', flat=True).distinct().order_by('brand')

    notes_set = set()
    for perfume in Perfumes.objects.all():
        if perfume.notes:
            notes_set |= extract_notes(perfume.notes)
    all_notes = sorted(notes_set, key=lambda s: s.lower())

    selected_brands = request.GET.getlist('brand')
    selected_notes = set(request.GET.getlist('note'))
    q = request.GET.get('q', '').strip()

    perfumes_qs = Perfumes.objects.all().order_by('?')

    if selected_brands:
        perfumes_qs = perfumes_qs.filter(brand__in=selected_brands)

    if selected_notes:
        filtered = []
        for p in perfumes_qs:
            if p.notes:
                perfume_notes = extract_notes(p.notes)
                if selected_notes & perfume_notes:
                    filtered.append(p)
        perfumes_qs = filtered

    if q:
        tmp_set = set()

        brand_name_results = perfumes_qs.filter(Q(brand__icontains=q) | Q(name__icontains=q))
        for p in brand_name_results:
            tmp_set.add(p)

        for p in perfumes_qs:
            if p.notes:
                perfume_notes = extract_notes(p.notes)
                if any(q.lower() in notes.lower() for notes in perfume_notes):
                    tmp_set.add(p)

        perfumes_qs = list(tmp_set)


    perfume_brand = request.GET.get('perfume_brand')

    if perfume_brand:

        perfumes_qs = Perfumes.objects.filter(brand=perfume_brand)


    paginator = Paginator(perfumes_qs, 16)
    page_number = request.GET.get('page') or 1
    perfumes_page = paginator.get_page(page_number)

    no_results = len(perfumes_page) == 0

    return render(request, 'perfume_app/perfumes_list.html', {
        'perfumes': perfumes_page,
        'all_brands': all_brands,
        'all_notes': all_notes,
        'selected_brands': selected_brands,
        'selected_notes': selected_notes,
        'no_results': no_results,
        'q': q,
    })


def perfume_detail(request, pk):
    perfume = Perfumes.objects.get(pk=pk)

    # 處理 notes
    if isinstance(perfume.notes, str):
        try:
            perfume.notes = json.loads(perfume.notes)
        except json.JSONDecodeError:
            perfume.notes = {}
    is_dict = isinstance(perfume.notes, dict)

    # 處理 main_accords
    if isinstance(perfume.main_accords, str):
        try:
            perfume.main_accords = json.loads(perfume.main_accords)
        except json.JSONDecodeError:
            perfume.main_accords = []

    is_list = isinstance(perfume.main_accords, list)

    # 取得該香水的評價列表
    reviews = Review.objects.filter(perfume=perfume).order_by('-created_at')

    avg_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0
    avg_rating = round(avg_rating * 2) / 2  # 四捨五入到0.5
    avg_whole = int(avg_rating)
    avg_half = (avg_rating - avg_whole) == 0.5

    # 取得用戶的所有訂單，以香水ID做 key，方便快速查詢
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user)
        order_perfume_ids = set(user_orders.values_list('perfume_id', flat=True))
    else:
        order_perfume_ids = set()

    context = {
        "perfume": perfume,
        "is_dict": is_dict,
        "is_list": is_list,
        "reviews": reviews,
        "star_range": range(1, 6),
        "avg_whole": avg_whole,
        "avg_half": avg_half,
        "order_perfume_ids": order_perfume_ids,
    }
    return render(request, 'perfume_app/perfume_detail.html', context)

@login_required
def submit_review(request, pk):

    perfume = get_object_or_404(Perfumes, pk=pk)

    if request.method == 'POST':
        gender = request.POST.get('gender')
        price_value = request.POST.get('price_value')
        rating = request.POST.get('rating')
        longevity = request.POST.get('longevity')
        sillage = request.POST.get('sillage')
        season = request.POST.get('season')
        content = request.POST.get('comment')

        review, created = Review.objects.update_or_create(
            user=request.user,
            perfume=perfume,
            defaults={
                'gender': gender,
                'price_value': price_value,
                'rating': rating,
                'longevity': longevity,
                'sillage': sillage,
                'season': season,
                'content': content,
            }
        )

        if created:
            profile = UserProfile.objects.get(user_id=request.user.id)
            if profile:
                profile.status = True
                profile.points += 1
                profile.save()

        return redirect('perfume_app:perfume_detail', pk=pk)

