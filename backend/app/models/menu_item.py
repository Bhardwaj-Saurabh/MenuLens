"""
Menu item and scan models for database
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class MenuScan(Base):
    """Represents a scanned menu session"""
    __tablename__ = "menu_scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=True)
    image_path = Column(String, nullable=False)

    # Menu metadata
    cuisine_type = Column(String, nullable=True)
    language = Column(String, nullable=True)
    restaurant_name = Column(String, nullable=True)

    # Analysis status
    status = Column(String, default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="menu_scans")
    items = relationship("MenuItem", back_populates="menu_scan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MenuScan {self.id} - {self.filename}>"


class MenuItem(Base):
    """Represents a single food item from a menu"""
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    menu_scan_id = Column(Integer, ForeignKey('menu_scans.id'), nullable=False)

    # Basic information
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(String, nullable=True)

    # Food classification
    food_type = Column(String, nullable=True)  # Vegetarian, Non-Vegetarian, Vegan, Unknown
    meat_type = Column(String, nullable=True)  # Chicken, Beef, Pork, Fish, Lamb, etc.
    contains_pork = Column(Boolean, default=False)
    contains_beef = Column(Boolean, default=False)

    # Ingredients and allergens
    ingredients = Column(JSON, nullable=True)  # List of ingredients
    allergens = Column(JSON, nullable=True)  # List of allergen names
    allergen_warnings = Column(JSON, nullable=True)  # Detailed allergen info

    # Image
    image_url = Column(String, nullable=True)
    image_source = Column(String, nullable=True)  # unsplash, google, etc.

    # AI confidence scores
    confidence_score = Column(Integer, nullable=True)  # 0-100

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    menu_scan = relationship("MenuScan", back_populates="items")

    def __repr__(self):
        return f"<MenuItem {self.name} ({self.food_type})>"
