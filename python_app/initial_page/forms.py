from django import forms

class PostnumberForm(forms.Form):
    your_pref = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'style':"width: 30%;height: 60%;font-size: 40px;"})
    )

class WorktimeForm(forms.Form):
    time_start = forms.TimeField(
        label='開始',
        required=True,
        widget=forms.TimeInput(attrs={'style':'font-size: 80px;width: 200%;text-align: center;','type':'time'}, format='%H:%M'))

    time_end = forms.TimeField(
        label='終了',
        required=True,
        widget=forms.TimeInput(attrs={'style':'font-size: 80px;width: 70%;text-align: center;','type':'time'},format='%H:%M'))
