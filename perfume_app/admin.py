from django.contrib import admin

from .models import Perfumes, Review


# Register your models here.
@admin.register(Perfumes)
class PerfumesAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','perfume','rating','content','created_at')

