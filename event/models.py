from django.db import models
import requests
from constance import config
from dateutil.parser import parse

class Location(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(unique=True, blank=True)
    about = models.TextField(blank=True, null=True)
    lont = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name  
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(unique=True, blank=True)

    def __str__(self):
        return self.name  
    
class City(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(unique=True, blank=True)

    def __str__(self):
        return self.name  

class Township(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=128)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name  
    
class Activity(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    township = models.ForeignKey(Township, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.CharField(unique=True, blank=True)
    url = models.CharField(max_length=600, blank=True, null=True)
    content = models.TextField(blank=True ,null=True)
    img_url = models.CharField(max_length=600, blank=True ,null=True)
    is_free = models.BooleanField(default=False)
    ticket_url = models.CharField(max_length=600, blank=True ,null=True)
    start_date = models.DateTimeField(blank=True , null=True)
    end_date = models.DateTimeField(blank=True , null=True)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def etkinlikleri_getir(take=200, skip=0):


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



                
     

            print()
        else:
            print("hata var", response.content)



            response = requests.get(
                url=base_url,
                params=params,
                headers=headers
            )

        if response.status_code in [200, 201]:
            data = response.json()
            print(data)  # Burada tüm API cevabını konsola yazdırır





           



            


        





     

    
    







      

