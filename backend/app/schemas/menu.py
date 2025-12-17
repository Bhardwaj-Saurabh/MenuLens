"""
Pydantic schemas for menu-related requests and responses
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class MenuItemAnalysis(BaseModel):
    """Schema for a single analyzed menu item"""
    name: str
    food_type: str = Field(..., description="Vegetarian, Non-Vegetarian, Vegan, or Unknown")
    meat_type: Optional[str] = Field(None, description="Type of meat if non-vegetarian")
    contains_pork: bool = False
    contains_beef: bool = False
    ingredients: List[str] = []
    allergens: List[str] = []
    image_url: Optional[str] = None


class MenuAnalysisResult(BaseModel):
    """Schema for complete menu analysis result"""
    menu_items: List[MenuItemAnalysis]
    cuisine_type: Optional[str] = None
    language: Optional[str] = None


class MenuAnalysisResponse(BaseModel):
    """Schema for API response after menu analysis"""
    success: bool
    filename: str
    analysis: MenuAnalysisResult


class MenuItemResponse(BaseModel):
    """Schema for database menu item response"""
    id: int
    name: str
    description: Optional[str]
    food_type: Optional[str]
    meat_type: Optional[str]
    contains_pork: bool
    contains_beef: bool
    ingredients: Optional[List[str]]
    allergens: Optional[List[str]]
    image_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class MenuScanResponse(BaseModel):
    """Schema for menu scan response"""
    id: int
    filename: str
    cuisine_type: Optional[str]
    language: Optional[str]
    status: str
    created_at: datetime
    items: List[MenuItemResponse] = []

    class Config:
        from_attributes = True
