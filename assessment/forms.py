from django import forms

class UserInfoForm(forms.Form):
    age = forms.IntegerField(min_value=10, max_value=120, initial=25)
    gender = forms.ChoiceField(choices=[('male','Male'),('female','Female'),('other','Other')])
    profession = forms.CharField(max_length=128)

class AnswersForm(forms.Form):
    answer_1 = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), required=True)
    answer_2 = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), required=True)
    answer_3 = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), required=True)
