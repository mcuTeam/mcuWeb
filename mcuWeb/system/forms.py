#coding:utf-8
import datetime

from django import forms
from django.forms import ModelForm, TextInput
from django.utils.translation import ugettext_lazy as _
from userena.forms import AuthenticationForm

from system.models import *

username_style = {'class': 'required'}

password_style = {'class': 'required'}


class SigninFormExtra(AuthenticationForm):
    identification = forms.CharField(label=_("Email or username"),
                                     widget=forms.TextInput(attrs=username_style),
                                     max_length=75,
                                     error_messages={'required': _("Either supply us with your email or username.")})
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(attrs=password_style, render_value=False))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(), required=False,
                                     label=_('Remember me for %(days)s') % {'days': 30})


class mcuAttributesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(mcuAttributesForm, self).__init__(*args, **kwargs)
        self.fields[u'curDate'] = forms.DateField(label=u"系统日期", initial=datetime.date.today(), required=True,
                                                 widget=forms.DateInput(attrs={u"type": u'date'})
                                                 )
        self.fields[u'curTime'] = forms.TimeField(label=u"系统时间", initial=datetime.datetime.now().time(), required=True,
                                                 widget=forms.TimeInput(attrs={u'type': u'time'})
                                                 )

    # curDate = forms.CharField(label='当前日期*',initial=datetime.date.today(),required=True)
    curDate = forms.DateField(label=u'1234', initial=datetime.date.today(), required=True)
    curTime = forms.TimeField(label=u'1234', initial=datetime.datetime.now().time(), required=True)

    class Meta:
        model = mcuAttributes
        fields = ['alias', 'logLevel', ]
        widgets = {
            'alias': TextInput(attrs={'class': 'text-input small-input', }),
            'logLevel': TextInput(attrs={'class': 'text-input small-input', }),
        }


class networkAdapterForm(forms.Form):
    Index = forms.IntegerField(label='Index', required=False)
    Description = forms.CharField(label='Description', max_length=100, required=False,
                                  widget=forms.TextInput(attrs={'class': 'text-input small-input', }))
    IP = forms.GenericIPAddressField(label='IP Address', required=True,
                                     widget=forms.TextInput(attrs={'class': 'text-input small-input', }))
    IPSubnet = forms.GenericIPAddressField(label='IPSubnet', required=True,
                                           widget=forms.TextInput(attrs={'class': 'text-input small-input', }))
    DefaultIPGateway = forms.GenericIPAddressField(label='DefaultIPGateway', required=True,
                                                   widget=forms.TextInput(attrs={'class': 'text-input small-input', }))


class gkModelForm(ModelForm):
    active = forms.BooleanField(label=u'是否启用GK', required=False)

    class Meta:
        model = gkAttributes
        fields = '__all__'


class gkForm(forms.Form):
    active = forms.BooleanField(label=u'是否启用GK', required=False)
    ip = forms.GenericIPAddressField(label='IP Address', required=True,
                                     widget=forms.TextInput(attrs={'class': 'text-input small-input', }))
    e164 = forms.CharField(label=u'E164号码', max_length=100, required=True,
                                  widget=forms.TextInput(attrs={'class': 'text-input small-input', }))

class uploadFileForm(forms.Form):
    file = forms.FileField(label=u"请选择上传文件：update.zip")
    # file.widget.attrs.update({'onchange':r'document.getElementById("textfield").value=this.value'})


class uploadConfigFileForm(forms.Form):
    file = forms.FileField(label=u"请选择配置文件：svcmmcu.ini")
    # file.widget.attrs.update({'onchange':r'document.getElementById("textfield").value=this.value'})
