from django.db import models
from admin_app.models import CustomUser

# Create your models here.
class Perfumes(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    launch_year = models.TextField(blank=True, null=True)
    main_accords = models.JSONField(blank=True, null=True)
    notes = models.JSONField(blank=True, null=True)
    longevity = models.JSONField(blank=True, null=True)
    sillage = models.JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'perfumes'

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    perfume = models.ForeignKey(Perfumes, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20)
    price_value = models.CharField(max_length=20)
    longevity = models.CharField(max_length=20)
    sillage = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'perfume')  # 用戶同香水不能有多筆評價




