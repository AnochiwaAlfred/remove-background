from django.conf import settings
from django.shortcuts import get_object_or_404
from ninja import File, Router, FormEx
from ninja.files import UploadedFile
from django.core.files.images import ImageFile
from users.models import *
from clean_image.models import *
from schemas.image_processor import *


import cv2              
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import rembg
import io
import os

router = Router(tags=["Processed Images Endpoints"])


# IMAGES ENDPOINTS

@router.post('image/process/')
def process3_image(request, user_id:str=FormEx(None), image: UploadedFile = FileEx(None)):
    input_content = image.read()
    inp = Image.open(io.BytesIO(input_content))
    output = rembg.remove(inp)
    output_filename = f"{uuid.uuid4()}.png"
    output.save(output_filename)
    # image_field_file = ImageFile(output)
    image_field_file = ImageFile(open(output_filename, "rb"))
    image_p = ProcessedImage.objects.create(user_id=user_id, image=image_field_file)
    image_p.save()
    os.remove(output_filename)
    inp.close()
    output.close()
    return {'message': 'Processing complete'}

@router.get('list_all_images/', response=List[ImageRetrievalSchema])
def list_images(request):
    """Get a list of all registered images"""
    images =  ProcessedImage.objects.all()
    imagesContainer = [ImageRetrievalSchema(
            id=imageS.id,
            user=imageS.user,
            created=imageS.created,
            image=request.build_absolute_uri(imageS.image.url)
    ) for imageS in images]
    return imagesContainer


@router.get('{user_id}/images/', response=List[ImageRetrievalSchema])
def list_all_user_images(request, user_id):
    """Get a list of all user images"""
    images =  ProcessedImage.objects.filter(user_id=user_id)
    imagesContainer = [ImageRetrievalSchema(
                id=imageS.id,
                user=imageS.user,
                created=imageS.created,
                image=request.build_absolute_uri(imageS.image.url)
        ) for imageS in images]
    return imagesContainer


@router.get('image/{image_id}/get/', response=ImageRetrievalSchema)
def get_image(request, image_id):
    """Get a specific image details"""
    image = get_object_or_404(ProcessedImage, id=image_id)
    return image

    
@router.delete('image/{image_id}/delete/')
def delete_message(request, image_id):
    """Delete a specific message"""
    image = get_object_or_404(ProcessedImage, id=image_id)
    if image:
        image.delete()
        return "Image {image.id} deleted successfully"
    return image




