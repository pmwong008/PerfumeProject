from django.db import models
from admin_app.models import CustomUser
from perfume_app.models import Perfumes

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    perfume = models.ForeignKey(Perfumes, on_delete=models.CASCADE)  # 新增這行
    perfume_name = models.CharField(max_length=100)
    perfume_brand = models.CharField(max_length=100)
    svg_value = models.CharField(max_length=50)
    name =  models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    post_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

