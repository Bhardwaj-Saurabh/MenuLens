"""
Allergen model for database
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.user import user_allergens


class Allergen(Base):
    """Allergen information model"""
    __tablename__ = "allergens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, default="medium")  # low, medium, high, severe

    # Common foods containing this allergen (stored as comma-separated string)
    common_sources = Column(Text, nullable=True)

    # Relationships
    users = relationship("User", secondary=user_allergens, back_populates="allergens")

    def __repr__(self):
        return f"<Allergen {self.name}>"
