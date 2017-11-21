# -*- coding: UTF-8 -*-
from system.models import *
from django.forms import ModelForm,ValidationError,TextInput
from django import forms

class terminalForm(ModelForm):
    class Meta:
        model = terminal
        fields = ['name','terminalIP',]
        widgets = {
        'name':TextInput(attrs={'class':'text-input small-input',}),
        'terminalIP':TextInput(attrs={'class':'text-input small-input',}),
        }

class meetingTemplateForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(meetingTemplateForm,self).__init__(*args,**kwargs)
        BANDWIDTH_CHOICES=[('512','512K'),
        ('1000','1M'),
        ('2000','2M'),
        ('3000','3M'),
        ('4000','4M'),
        ('6000','6M'),
        ('8000','8M')
        ]
        VIDEOPROTOCOL_CHOICES=[
        ('H.264','H.264'),
        ('H.263','H.263')
        ]
        VIDEOFRAMERATE_CHOICES=[
        ('25','25FPS'),
        ('30','30FPS'),
        ('60','60FPS')
        ]
        CAPALITYNAME_CHOICES=[
        ('1080P','1080P'),
        ('720P','720P'),
        ('CIF','CIF')
        ]
        AUDIOPROTOCOL_CHOICES=[
        ('G.711-ulaw','G.711-ulaw'),
        ('G.711-alaw','G.711-alaw'),
        ]
        self.fields['bandwidth'] = forms.ChoiceField(label="带宽*",choices=BANDWIDTH_CHOICES,initial=('4000','4M'),required=True)
        self.fields['videoProtocol'] = forms.ChoiceField(label="视频协议*",choices=VIDEOPROTOCOL_CHOICES,initial=('H.264','H.264'),required=True)
        self.fields['videoFrameRate'] = forms.ChoiceField(label="视频刷新率*",choices=VIDEOFRAMERATE_CHOICES,initial=('60','60FPS'),required=True)
        self.fields['capalityname'] = forms.ChoiceField(label="视频分辨率*",choices=CAPALITYNAME_CHOICES,initial=('1080P','1080P'),required=True)
        self.fields['audioProtocol'] = forms.ChoiceField(label="音频协议*",choices=AUDIOPROTOCOL_CHOICES,initial=('G.711-ulaw','G.711-ulaw'),required=True)


    class Meta:
        model = meetingTemplate
        fields = '__all__'

class meetingForm(ModelForm):
    class Meta:
        model = meeting
        fields = '__all__'
