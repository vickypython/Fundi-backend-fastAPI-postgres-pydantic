# app/schemas/user.py
from pydantic import BaseModel, EmailStr,Field
from typing import Optional,List
from enum import Enum
from datetime import datetime
from uuid import UUID


class UserRole(str,Enum):
    client="client"
    fundi="fundi"
    admin="admin"
class JobStatus(str,Enum):
    open="open"
    accepted="accepted"
    completed="completed"
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role:UserRole
    location=Optional[str]=None
    

class UserCreate(UserBase):
    password: str
   
class UserOut(BaseModel):
    id:UUID
    profile_picture:Optional[str]=None
    class config:
        from_attribute=True
class FundiProfileBase(BaseModel):
    daily_rate:float
    availability:Optional[str]=None
    portfolio_items:Optional[List[str]]=[]
    conditions :Optional[str]=None
class FundiProfileCreate(FundiProfileBase):
    user_id:UUID
class FundiProfileResponse(FundiProfileBase):
    id:UUID
    average_rating:Optional[float]
    class config:
        from_attribute=True
class HomeOwnProfileBase(BaseModel):
    bio:Optional[str]=None
    address:Optional[str]=None
    preferred_payment_method:Optional[str]=None
class HomeOwnProfileCreate(HomeOwnProfileBase):
    user_id:UUID
class HomeOwnProfileResponse(HomeOwnProfileBase):
    id:UUID
    class config:
        from_attribute=True
class JobPostingBase(BaseModel):
    job_description: str
    location: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None
    status: JobStatus = JobStatus.open

class JobPostingCreate(JobPostingBase):
    client_id: UUID

class JobPostingResponse(JobPostingBase):
    id: UUID

    class Config:
        from_attribute = True
class MessageBase(BaseModel):
    message:str
class MessageCreate(MessageBase):
    sender_id:UUID
    receiver_id:UUID
class MessageResponse(MessageBase):
    id:UUID
    sender_id:UUID
    receiver_id:UUID
    timestamp:datetime
    class config:
        from_attribute=True
class RatingBase(BaseModel):
    rating: float
    review: Optional[str] = None

class RatingCreate(RatingBase):
    job_id: UUID
    rated_by: UUID
    fundi_id: UUID

class RatingResponse(RatingBase):
    id: UUID
    job_id: UUID
    rated_by: UUID
    fundi_id: UUID

    class Config:
        from_attribute = True







