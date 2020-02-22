from django.db import models

# Create your models here.
class Customer(models.Model):
    # id = AutoField(primary_key=True)  # 自動的に追加されるので定義不要
    post_number = models.CharField(max_length=7)
    prefecture = models.CharField(max_length=10)
    time_start = models.TimeField(widget=forms.TimeInput(format='%H:%M'))
    time_end = models.TimeField(widget=forms.TimeInput(format='%H:%M'))
    scale = models.IntegerField(max_length=1)