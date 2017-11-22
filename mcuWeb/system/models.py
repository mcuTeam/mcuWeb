# coding=utf-8
from django.db import models

# Create your models here.

class terminal(models.Model):
	name = models.IntegerField(blank=False,null=False,verbose_name=u"E164 Alias*")
	terminalIP = models.GenericIPAddressField(unique=True,max_length=200,blank=False,null=False,verbose_name=u"IP*",error_messages={'unique':u"重复IP,请重新输入!"})

class meetingTemplate(models.Model):
	name = models.CharField(unique=True,max_length=200,blank=False,null=False,verbose_name="会议模板名称*")
	bandwidth = models.CharField(max_length=200,blank=False,null=False,default="4000",verbose_name="带宽*")
	videoProtocol = models.CharField(max_length=200,blank=False,null=False,default="H.264",verbose_name="视频协议*")
	videoFrameRate = models.IntegerField(blank=False,null=False,default=60,verbose_name=u"视频刷新率*")
	capalityname = models.CharField(max_length=200,blank=False,null=False,default="1080P",verbose_name="视频分辨率*")
	audioProtocol = models.CharField(max_length=200,blank=False,null=False,default="G.711-ulaw",verbose_name="音频协议*")

class meeting(models.Model):
	name = models.CharField(unique=True,max_length=200,blank=False,null=False,verbose_name="会议名称*")
	meetcode = models.CharField(unique=True,max_length=200,blank=False,null=False,verbose_name="会议编号*")
	remark = models.CharField(max_length=400,blank=True,null=False,default="",verbose_name="备注")

	bandwidth = models.CharField(max_length=200,blank=False,null=False,default="4000",verbose_name="带宽*")
	videoProtocol = models.CharField(max_length=200,blank=False,null=False,default="H.264",verbose_name="视频协议*")
	videoFrameRate = models.IntegerField(blank=False,null=False,default=60,verbose_name=u"视频刷新率*")
	capalityname = models.CharField(max_length=200,blank=False,null=False,default="1080P",verbose_name="视频分辨率*")
	audioProtocol = models.CharField(max_length=200,blank=False,null=False,default="G.711-ulaw",verbose_name="音频协议*")
