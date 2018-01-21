from django import forms


class StyleUploadForm(forms.Form):
    styles = forms.FileField(required=True,
                             widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                    'accept': '.sld'}))
