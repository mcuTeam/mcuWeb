# coding=utf-8
from django.db import models

# Create your models here.

class terminal(models.Model):
	name = models.IntegerField(blank=False,null=False,verbose_name=u"E164 Alias")
	terminalIP = models.GenericIPAddressField(unique=True,max_length=200,blank=False,null=False,verbose_name=u"IP",error_messages={'unique':u"重复IP,请重新输入!"})

class meetingTemplate(models.Model):
	name = models.CharField(unique=True,max_length=200,blank=False,null=False,verbose_name=u"meetingTemplate名称")
	bandwidth = models.CharField(max_length=200,blank=False,null=False,default="4M",verbose_name=u"bandwidth")

class meeting(models.Model):
	name = models.CharField(unique=True,max_length=200,blank=False,null=False,verbose_name=u"meeting name")
	meetcode = models.CharField(unique=True,max_length=200,blank=False,null=False,verbose_name=u"meeting code")
	remark = models.CharField(max_length=400,blank=True,null=False,default="",verbose_name="remark")
