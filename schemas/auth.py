from ninja import Schema, FileEx, UploadedFile
from typing import List
from datetime import date, datetime




class AuthUserRegistrationSchema(Schema):
    email:str=None
    username:str=None    


class AuthUserRetrievalSchema(Schema):
    id:int=None
    email:str=None
    username:str=None    
    is_staff:bool=None
    
    
class UserLoginSchema(Schema):
    email: str=None
    password: str=None
    
class AuthUserStatusRetrievalSchema(Schema):
    id:int=None
    email:str=None
    username:str=None    
    is_active:bool=None
    is_staff:bool=None
    is_superuser:bool=None
    
    
    
    
