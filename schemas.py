"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogpost" collection
- Confession -> "confession" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Existing example schemas
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Scrapp-specific schemas
class BlogPost(BaseModel):
    username: str = Field(..., description="Author username")
    avatar_url: Optional[str] = Field(None, description="URL to user avatar")
    content: str = Field(..., description="Blog content text")
    reactions: Optional[List[str]] = Field(default_factory=list, description="List of emoji reaction codes")

class Confession(BaseModel):
    content: str = Field(..., description="Anonymous confession text")
    mood: Optional[str] = Field(None, description="Optional mood tag")
    support: int = Field(0, ge=0, description="Support count")
    hug: int = Field(0, ge=0, description="Hug count")
    laugh: int = Field(0, ge=0, description="Laugh count")
