from django.db import models

# Create your models here.
class category(models.Model):
    category_name = models.CharField(max_length=100)

class products(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    price= models.IntegerField()
    description= models.CharField(max_length=500)
    image = models.ImageField(null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url= self.image.url
        except:
            url=''
        return url

# class cart(models.Model):
    