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
        BANDWIDTH_CHOICES=[('512K','512K'),
        ('1M','1M'),
        ('2M','2M'),
        ('3M','3M'),
        ('4M','4M'),
        ('6M','6M'),
        ('8M','8M')
        ]
        self.fields['bandwidth'] = forms.ChoiceField(label="daikuan",choices=BANDWIDTH_CHOICES,required=True)
    class Meta:
        model = meetingTemplate
        fields = '__all__'

class meetingForm(ModelForm):
    class Meta:
        model = meeting
        fields = '__all__'
