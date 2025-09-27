from django.contrib import admin

from ai_app.models import Order

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','perfume_name','perfume_brand','svg_value','name','address','post_status','created_at')

