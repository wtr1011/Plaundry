from django.db import models

# Create your models here.
class Customer(models.Model):
    # id = AutoField(primary_key=True)  # 自動的に追加されるので定義不要
    post_number = models.CharField('郵便番号',max_length=7)
    prefecture = models.CharField('都道府県',max_length=10)
    time_start = models.TimeField('仕事開始時間')
    time_end = models.TimeField('仕事終了時間')
    scale = models.IntegerField('洗濯機の大きさ')