from django import forms
from .models import Activity,Category,Location,City,Township

class ActivityForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset = Category.objects.all(),
        empty_label = "Kategori Seçiniz",
        widget = forms.Select(attrs={'class':'form-control'})
    )

    location = forms.ModelChoiceField(
        queryset = Location.objects.all(),
        empty_label = "Yer Seçiniz",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    township = forms.ModelChoiceField(
        queryset = Township.objects.all(),
        empty_label = "İlçe Seçiniz",
        widget=forms.Select(attrs={'class':'form-control'})
    )

    class Meta:
        model = Activity
        fields = [
            'name', 'slug', 'content', 'start_date', 'end_date', 'location', 'category', 'township', 'is_free', 'ticket_url', 'url', 'img_url'

        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Etkinlik Adı'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL Adresi'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Etkinlik Açıklaması'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}), 
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ticket_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Bilet Satış URL '}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Etkinlik Web Sitesi'}),
            'img_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Görsel URL'}),
        }
        labels = { 
            'name': 'Etkinlik Adı',
            'slug': 'URL Adresi',
            'content': 'Açıklama',
            'start_date': 'Başlangıç Tarihi ve Saati',
            'end_date': 'Bitiş Tarihi ve Saati',
            'is_free': 'Ücretsiz mi?',
            'ticket_url': 'Bilet Linki',
            'url': 'Dış Link',
            'img_url': 'Görsel Linki',
            'location': 'Yer',
            'category': 'Kategori',
            'township': 'İlçe',
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['slug'].required = False
        
