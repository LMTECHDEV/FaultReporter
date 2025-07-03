from django.db import models

class Fault(models.Model):
    location = models.CharField(max_length=200)
    description = models.TextField()
    image1 = models.ImageField(upload_to='faults/')
    image2 = models.ImageField(upload_to='faults/', blank=True, null=True)
    image3 = models.ImageField(upload_to='faults/', blank=True, null=True)
    image4 = models.ImageField(upload_to='faults/', blank=True, null=True)
    image5 = models.ImageField(upload_to='faults/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.created_at}"