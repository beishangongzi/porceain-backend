import os

from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=10)
    price = models.IntegerField()



import uuid
#提取出公共的方法evaluation_directory_path获取图片后缀
# 使用uuid创建唯一的图片名，并保存的路径和文件名一并返回
def evaluation_directory_path(product_id, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("evaluations", filename)

class ProductEvaluationImage(models.Model):
    images = models.FileField(null=True, blank=True,
                                  upload_to=evaluation_directory_path,
                                  verbose_name="商品评价图片")
    class Meta:
        verbose_name = "商品评价关联图"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.images.name
