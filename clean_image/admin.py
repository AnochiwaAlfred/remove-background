from django.contrib import admin
from clean_image.models import ProcessedImage

# Register your models here.

@admin.register(ProcessedImage)
class ProcessedimageAdmin(admin.ModelAdmin):
    pass