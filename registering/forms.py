from django import forms

class MemberForm(forms.Form):
    english_name = forms.CharField(label='Your english name', max_length=150)
    chinese_name = forms.CharField(label='Your chinese name',max_length=150, required= False)
    email = forms.CharField(label='Your email',max_length=150)
    password1 = forms.CharField(label='Your password')
    password2 = forms.CharField(label='Your password')
    student_id = forms.IntegerField()