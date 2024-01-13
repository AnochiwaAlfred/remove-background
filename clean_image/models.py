from django.db import models
from core.core import CoreBaseModel
from plugins.generate_filename import generate_filename
# Create your models here.

class ProcessedImage(CoreBaseModel):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='processedImages/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Processed Image"
        verbose_name_plural = "Processed Images"