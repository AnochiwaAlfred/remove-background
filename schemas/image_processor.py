import json
import uuid
from ninja import Schema, File
from typing import List
from datetime import datetime
from schemas.auth import *        
    


class ImageRetrievalSchema(Schema):
    id:uuid.UUID=None
    user:AuthUserRetrievalSchema=None
    created:datetime=None
    image:str=None
    
    


    
    

    
    
