from django.db import models

"""
blank=True、null=True。统一的表明了该字段（列）是可以为空的。
blank=False、null=False。统一的表面了该字段（列）不可以为空。
blank=True、null=False。这个设定的意义在于，某些字段并不希望用户在表单中创建（如slug），而是通过在save方法中根据其他字段生成。
blank=False、null=True。这个设定不允许表单中该字段为空，但是允许在更新时或者通过shell等非表单方式插入数据该字段为空。
"""


class UserInfo(models.Model):
    phone = models.CharField(verbose_name='手机号', max_length=11, unique=True)
    token = models.CharField(verbose_name='用户TOKEN', max_length=64, null=True, blank=True)
