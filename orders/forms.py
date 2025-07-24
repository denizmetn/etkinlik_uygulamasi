from django import forms
from .models import Order

class OrderForm(forms.Form):
    quantity_standart = forms.IntegerField(label="Tam Bilet", min_value=0, initial=0)
    quantity_student = forms.IntegerField(label="Öğrenci Bileti", min_value=0, initial=0)
    quantity_vip = forms.IntegerField(label="VIP Bilet", min_value=0, initial=0)

    def clean(self):
        cleaned_data = super().clean()
        total = (
            cleaned_data.get('quantity_standart', 0) +
            cleaned_data.get('quantity_student', 0) +
            cleaned_data.get('quantity_vip', 0)
        )
        if total == 0:
            raise forms.ValidationError("En az bir bilet tipi seçmelisiniz.")
        return cleaned_data
 
