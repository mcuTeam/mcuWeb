# -*- coding: UTF-8 -*-
import datetime

from django import forms
from django.forms import ModelForm, TextInput

from system.models import *


class terminalForm(ModelForm):
    class Meta:
        model = terminal
        fields = ['name', 'terminalIP', ]
        widgets = {
            'name': TextInput(attrs={'class': 'text-input small-input', }),
            'terminalIP': TextInput(attrs={'class': 'text-input small-input', }),
        }


class meetingTemplateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(meetingTemplateForm, self).__init__(*args, **kwargs)
        BANDWIDTH_CHOICES = [('512', '512K'),
                             ('1000', '1M'),
                             ('2000', '2M'),
                             ('3000', '3M'),
                             ('4000', '4M'),
                             ('6000', '6M'),
                             ('8000', '8M')
                             ]
        VIDEOPROTOCOL_CHOICES = [
            ('H.264', 'H.264'),
            ('H.263', 'H.263')
        ]
        VIDEOFRAMERATE_CHOICES = [
            ('25', '25FPS'),
            ('30', '30FPS'),
            ('60', '60FPS')
        ]
        CAPALITYNAME_CHOICES = [
            ('1080P', '1080P'),
            ('720P', '720P'),
            ('CIF', 'CIF')
        ]
        AUDIOPROTOCOL_CHOICES = [
            ('G.711-ulaw', 'G.711-ulaw'),
            ('G.711-alaw', 'G.711-alaw'),
        ]
        self.fields['bandwidth'] = forms.ChoiceField(label="带宽*", choices=BANDWIDTH_CHOICES, initial=('4000', '4M'),
                                                     required=True)
        self.fields['videoProtocol'] = forms.ChoiceField(label="视频协议*", choices=VIDEOPROTOCOL_CHOICES,
                                                         initial=('H.264', 'H.264'), required=True)
        self.fields['videoFrameRate'] = forms.ChoiceField(label="视频刷新率*", choices=VIDEOFRAMERATE_CHOICES,
                                                          initial=('60', '60FPS'), required=True)
        self.fields['capalityname'] = forms.ChoiceField(label="视频分辨率*", choices=CAPALITYNAME_CHOICES,
                                                        initial=('1080P', '1080P'), required=True)
        self.fields['audioProtocol'] = forms.ChoiceField(label="音频协议*", choices=AUDIOPROTOCOL_CHOICES,
                                                         initial=('G.711-ulaw', 'G.711-ulaw'), required=True)

    class Meta:
        model = meetingTemplate
        fields = '__all__'


class meetingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(meetingForm, self).__init__(*args, **kwargs)
        OPERATIONMODEL_CHOICES = [
            ('操作员模式', '操作员模式'),
            # ('主席模式','主席模式'),
            # ('语音激励模式','语音激励模式')
        ]
        self.fields['name'] = forms.CharField(label='会议名称*', initial=datetime.date.today(), required=True)
        self.fields['meetcode'] = forms.CharField(label='会议编号*', initial=datetime.date.today(), required=True)
        self.fields['template'].choices = [(x.pk, x.name) for x in meetingTemplate.objects.all()]
        self.fields['mainMeetRoom'] = forms.ChoiceField(label="主会场*",
                                                        choices=[(x.pk, x.name) for x in terminal.objects.all()],
                                                        required=True, \
                                                        error_messages={"invalid_choice": "该终端不存在，请刷新页面"})
        self.fields['operationModel'] = forms.ChoiceField(label="操作模式*", choices=OPERATIONMODEL_CHOICES,
                                                          initial=('操作员模式', '操作员模式'), required=True)
        # template = forms.ChoiceField(label="会议模板*",choices=[(x.pk, x.name) for x in meetingTemplate.objects.all()],initial=('1','1'),required=True)

    template = forms.ChoiceField(label="会议模板*", required=True)

    def clean_template(self):
        templatePK = self.cleaned_data['template']
        if not meetingTemplate.objects.filter(pk=int(templatePK)).exists():
            raise forms.ValidationError("模板不存在")
        return templatePK

    def clean_mainMeetRoom(self):
        print("clean_mainMeetRoom")
        terminalPK = self.cleaned_data['mainMeetRoom']
        if not terminal.objects.filter(pk=int(terminalPK)).exists():
            raise forms.ValidationError("该终端不存在")
        return terminalPK

    def save(self, commit=True):
        meeting = super(meetingForm, self).save(commit=False)
        template = meetingTemplate.objects.get(pk=self.cleaned_data['template'])
        meeting.bandwidth = template.bandwidth
        meeting.videoProtocol = template.videoProtocol
        meeting.videoFrameRate = template.videoFrameRate
        meeting.capalityname = template.capalityname
        meeting.audioProtocol = template.audioProtocol

        meeting.dualProtocol = template.dualProtocol
        meeting.dualFormat = template.dualFormat
        meeting.dualBandWidth = template.dualBandWidth

        terminalInstance = terminal.objects.get(pk=self.cleaned_data['mainMeetRoom'])
        meeting.mainMeetRoomName = terminalInstance.name

        if commit:
            meeting.save()
        return meeting

    class Meta:
        model = meeting
        fields = ['name',
                  'meetcode',
                  'mainMeetRoom',
                  'operationModel',
                  'remark'
                  ]
