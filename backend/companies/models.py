from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random

class Company(models.Model):
    vendors=models.ManyToManyField(User,blank=True,related_name="vendors")
    staff=models.ManyToManyField(User,blank=True,related_name="staff")
    collaborators=models.ManyToManyField(User,blank=True,related_name="collaborators")
    vid=models.CharField(max_length=10,blank=True)
    name=models.CharField(max_length=50)
    vat=models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=2)
    country = models.CharField(max_length=2,default="IT")
    cap = models.CharField(max_length=5)
    address = models.CharField(max_length=50)
    pec=models.EmailField(blank=True)
    sdi=models.CharField(max_length=11,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.vid=generate_vid()
        super(Company, self).save(*args, **kwargs)
    


def generate_vid():
    vid_list=Company.objects.all().values_list('vid',flat=True)
    def random_string():
        letters = ''.join((random.choice(string.ascii_letters) for i in range(8))).upper()
        digits = ''.join((random.choice(string.digits) for i in range(2)))
        sample_list = list(letters + digits)
        random.shuffle(sample_list)
        generated = ''.join(sample_list)
        return generated
    generated=random_string()
    while(generated in vid_list):
        generated=random_string
    return generated