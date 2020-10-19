from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import User
# Create your models here.



class bill(models.Model):
    billno = models.CharField(max_length=200)
    item = models.CharField(max_length=2000)
    date = models.DateField()
    amount = models.IntegerField()
    remark = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.billno


class billformDetail(ModelForm):
    
    class Meta:
        model = bill
        fields = ['billno','item','date','amount','remark']
        labels = {
            'billno':_('Bill Number'),'item':_('Item'),'date':_('Date'),'amount':_('Amount'),'remark':_('Remark'),
        }
        widgets = {
            'date': forms.DateInput(format=('%d-%m-%Y'), attrs={'firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date'}),
        }