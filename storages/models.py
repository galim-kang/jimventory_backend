# storage/models.py
from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL을 사용하기 위함

class Storage(models.Model):
    hostUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='storages')
    storeType = models.CharField(max_length=50)
    serviceName = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    operatingTime = models.JSONField()  # ["1000", "2300"] 형식
    description = models.JSONField()  # ["3층", "엘레베이터 있음"] 형식
    introduction = models.TextField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='storage_images/', blank=True)  # 이미지 필드
    contact_info = models.CharField(max_length=100)  # 연락처 정보

    def __str__(self):
        return self.serviceName

class Menu(models.Model):
    storage = models.ForeignKey(Storage, related_name='menus', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')  # 이미지 필드

    def __str__(self):
        return self.name
