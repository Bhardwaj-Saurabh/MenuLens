"""
User model for database
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Association table for user allergies (many-to-many)
user_allergens = Table(
    'user_allergens',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('allergen_id', Integer, ForeignKey('allergens.id'))
)


class User(Base):
    """User model with dietary preferences and allergies"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Profile information
    full_name = Column(String, nullable=True)

    # Dietary preferences
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_halal = Column(Boolean, default=False)
    is_kosher = Column(Boolean, default=False)
    avoid_pork = Column(Boolean, default=False)
    avoid_beef = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    allergens = relationship("Allergen", secondary=user_allergens, back_populates="users")
    menu_scans = relationship("MenuScan", back_populates="user")
