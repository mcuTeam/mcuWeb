# coding=utf-8
from django.db import models


# Create your models here.

class terminal(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False, null=False, verbose_name=u"E164 Alias*")
    terminalIP = models.GenericIPAddressField(unique=True, max_length=200, blank=False, null=False, verbose_name=u"IP*",
                                              error_messages={'unique': u"重复IP,请重新输入!"})
    capalityname = models.CharField(max_length=200, blank=False, null=False, default="1080P", verbose_name=u"视频分辨率*")


class meetingTemplate(models.Model):
    name = models.CharField(unique=True, max_length=200, blank=False, null=False, verbose_name=u"会议模板名称*")
    bandwidth = models.CharField(max_length=200, blank=False, null=False, default="4000", verbose_name=u"带宽*")
    videoProtocol = models.CharField(max_length=200, blank=False, null=False, default="H.264", verbose_name=u"视频协议*")
    videoFrameRate = models.IntegerField(blank=False, null=False, default=60, verbose_name=u"视频刷新率*")
    capalityname = models.CharField(max_length=200, blank=False, null=False, default="1080P", verbose_name=u"视频分辨率*")
    audioProtocol = models.CharField(max_length=200, blank=False, null=False, default="G.711-ulaw",
                                     verbose_name=u"音频协议*")

    dualProtocol = models.CharField(max_length=200, blank=False, null=False, default="H.264", verbose_name=u"双流视频协议*")
    dualFormat = models.CharField(max_length=200, blank=False, null=False, default="XGA", verbose_name=u"双流视频格式*")
    dualBandWidth = models.IntegerField(blank=False, null=False, default=1024, verbose_name=u"双流带宽*")


class meeting(models.Model):
    name = models.CharField(unique=True, max_length=200, blank=False, null=False, verbose_name=u"会议名称*")
    meetcode = models.CharField(unique=True, max_length=200, blank=False, null=False, verbose_name=u"会议编号*")
    remark = models.CharField(max_length=400, blank=True, null=False, default="", verbose_name=u"备注")

    activeInMcu = models.BooleanField(default=True, verbose_name=u"是否在mcu列表中")

    bandwidth = models.CharField(max_length=200, blank=False, null=False, default="4000", verbose_name=u"带宽*")
    videoProtocol = models.CharField(max_length=200, blank=False, null=False, default="H.264", verbose_name=u"视频协议*")
    videoFrameRate = models.IntegerField(blank=False, null=False, default=60, verbose_name=u"视频刷新率*")
    capalityname = models.CharField(max_length=200, blank=False, null=False, default="1080P", verbose_name=u"视频分辨率*")
    audioProtocol = models.CharField(max_length=200, blank=False, null=False, default="G.711-ulaw",
                                     verbose_name=u"音频协议*")

    dualProtocol = models.CharField(max_length=200, blank=False, null=False, default="H.264", verbose_name=u"双流视频协议*")
    dualFormat = models.CharField(max_length=200, blank=False, null=False, default="XGA", verbose_name=u"双流视频格式*")
    dualBandWidth = models.IntegerField(blank=False, null=False, default=1024, verbose_name=u"双流带宽*")

    mainMeetRoom = models.CharField(max_length=200, blank=False, null=False, default="", verbose_name=u"主会场*")
    mainMeetRoomName = models.CharField(max_length=200, blank=False, null=False, default="", verbose_name=u"主会场名称*")
    operationModel = models.CharField(max_length=200, blank=False, null=False, default=u"操作员模式", verbose_name=u"操作模式*")


class mcuAttributes(models.Model):
    alias = models.CharField(unique=True, max_length=200, blank=False, null=False, verbose_name=u"MCU别名*")
    logLevel = models.IntegerField(blank=False, null=False, default=0, verbose_name=u"日志级别*")


class gkAttributes(models.Model):
    ip = models.GenericIPAddressField(unique=True, max_length=200, blank=False, null=False, verbose_name=u"IP*")
    active = models.BooleanField(default=False)
