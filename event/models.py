from django.db import models
import requests
from constance import config
from dateutil.parser import parse
from django.template.defaultfilters import slugify 
from account.models import CustomUser 
from django.conf import settings

class Location(models.Model):
    name = models.CharField(max_length=200, verbose_name="Yer Adı")
    slug = models.CharField(unique=True, blank=True, verbose_name="URL Dostu İsim")
    about = models.TextField(blank=True, null=True, verbose_name="Hakkında")
    lont = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Enlem")
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Boylam")

    class Meta:
        verbose_name = "Yer"
        verbose_name_plural = "Yerleşimler"

    def __str__(self):
        return self.name  

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)    
    
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategori Adı")
    slug = models.CharField(unique=True, blank=True, verbose_name="URL Dostu İsim")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name  

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class City(models.Model):
    name = models.CharField(max_length=200, verbose_name="Şehir Adı")
    slug = models.CharField(unique=True, blank=True, verbose_name="URL Dostu İsim")

    class Meta:
        verbose_name = "Şehir"
        verbose_name_plural = "Şehirler"
    
    def __str__(self):
        return self.name  

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Township(models.Model):
    name = models.CharField(max_length=200, verbose_name="İlçe Adı")
    slug = models.CharField(max_length=128, blank=True, verbose_name="URL Dostu İsim")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Şehir")

    class Meta:
        verbose_name = "İlçe"
        verbose_name_plural = "İlçeler"
        unique_together = ('slug', 'city')

    def __str__(self):
        return self.name  

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
class Activity(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE,verbose_name="Yer")
    category = models.ForeignKey(Category,on_delete=models.CASCADE, verbose_name="Kategori")
    township = models.ForeignKey(Township, on_delete=models.CASCADE, verbose_name="İlçe")
    organizer = models.ForeignKey('account.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='organized_activities', verbose_name="Organizatör")
    name = models.CharField(max_length=200, verbose_name="Etkinlik Adı")
    slug = models.CharField(unique=True, blank=True, verbose_name="URL Dostu İsim")
    url = models.CharField(max_length=600, blank=True, null=True, verbose_name="Etkinlik URL'i")
    content = models.TextField(blank=True ,null=True, verbose_name="İçerik")
    img_url = models.CharField(max_length=600, blank=True ,null=True, verbose_name="Görsel URL'i")
    is_free = models.BooleanField(default=False, verbose_name="Ücretsiz Mi?")
    ticket_url = models.CharField(max_length=600, blank=True ,null=True, verbose_name="Bilet URL'i")
    start_date = models.DateTimeField(blank=True , null=True, verbose_name="Başlangıç Tarihi")
    end_date = models.DateTimeField(blank=True , null=True, verbose_name="Bitiş Tarihi")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi") 
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi") 
    is_published = models.BooleanField(default=True, verbose_name="Yayınlandı mı?")
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Etkinlik"
        ordering = ['start_date']

    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.name)
            original_slug = self.slug
            count = 1
            while Activity.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{count}"
                count += 1
        super().save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'activity')

    def __str__(self):
        return f"{self.user.username} favorited {self.activity.name}"


    
    @staticmethod
    def etkinlikleri_getir(take=280, skip=0):

        base_url = "https://backend.etkinlik.io/api/v2/events"

        params = {
            "take": take,
            "skip": skip
        }

        headers = {
            "X-Etkinlik-Token": config.API_KEY
        }

        response = requests.get(
            url=base_url,
            params=params,
            headers=headers
        )

        if response.status_code in [200, 201]:
            data = response.json()
            items = data.get("items")
            for row in items:
                name = row.get("name")
                slug = row.get("slug")
                content = row.get("content")


                category = None
                location = None
                township = None

                venue = row.get("venue")
                if venue:
                    location, cr = Location.objects.get_or_create(slug=venue.get("slug"))
                    location.name = venue.get("name")
                    location.about = venue.get("about")
                    location.lont = venue.get("lat")
                    location.long = venue.get("lng")
                    location.save()
                
                category_dict = row.get("category")
                print("category_dict>>>",category_dict)
                if category_dict:
                    category, cr = Category.objects.get_or_create(slug=category_dict.get("slug"))
                    category.name=category_dict.get("name")
                    category.save()
                
                city_dict = venue.get("city")
                if city_dict:
                    city, cr = City.objects.get_or_create(slug=city_dict.get("slug"))
                    city.name=city_dict.get("name")
                    city.save()

                    township_dict = venue.get("district")
                    if township_dict:
                        township, cr = Township.objects.get_or_create(
                            slug=township_dict.get("slug"),
                            city=city
                        )
                        township.name = township_dict.get("name")
                        township.save()
                
                etkinlik = Activity.objects.filter(slug=row.get("slug")).first()
                if not etkinlik:
                    etkinlik = Activity()
                    etkinlik.slug = slug

                etkinlik.location = location
                etkinlik.township = township
                etkinlik.category = category
                etkinlik.name = name
                etkinlik.slug = slug
                etkinlik.content = content
                etkinlik.url = row.get("url")
                etkinlik.img_url = row.get("poster_url")
                etkinlik.ticket_url = row.get("ticket_url")
                etkinlik.is_free = row.get("is_free") in ["True", True, "true"]

                start = row.get("start")
                end = row.get("end")
                etkinlik.start_date = parse(start) if start else None
                etkinlik.end_date = parse(end) if end else None
                
                etkinlik.save()

        else:
            print("hata var", response.content)


        





           



            


        





     

    
    







      

