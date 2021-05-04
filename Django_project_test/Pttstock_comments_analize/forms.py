from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    your_email = forms.CharField(label='Your email', max_length=100)


class DateForm(forms.Form):
    # search_date = forms.DateField(label='Date ')
    search_date = forms.DateField(
        label="Date",
        widget=forms.DateInput(attrs={'class': 'form-control', "required": 'required', "type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
