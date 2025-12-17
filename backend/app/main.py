"""
MenuLens Backend - Main FastAPI Application
"""
import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import aiofiles

from app.core.config import settings
from app.core.ai_service import ai_service
from app.core.image_search_service import image_search_service
from app.db.database import get_db, init_db

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.on_event("startup")
async def startup_event():
    """Initialize database and other services on startup"""
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📁 Upload directory: {UPLOAD_DIR}")
    print(f"🤖 AI Provider: {settings.AI_PROVIDER}")
    print(f"🎨 Image Generation: {'DALL-E 3 ✓' if settings.OPENAI_API_KEY else 'Not configured'}")
    # Uncomment when database models are ready
    # init_db()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "MenuLens API is running",
        "version": settings.APP_VERSION,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "ai_provider": settings.AI_PROVIDER
    }


def validate_image(file: UploadFile) -> None:
    """Validate uploaded image file"""
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # Note: File size validation happens during upload
    # FastAPI doesn't provide content-length before reading the file


@app.post("/api/menu/upload")
async def upload_menu_image(file: UploadFile = File(...)):
    """
    Upload a menu image for analysis
    Returns the file path for later processing
    """
    try:
        # Validate file
        validate_image(file)

        # Generate unique filename
        import uuid
        file_ext = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename

        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()

            # Check file size
            if len(content) > settings.MAX_UPLOAD_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
                )

            await f.write(content)

        return {
            "message": "File uploaded successfully",
            "filename": unique_filename,
            "file_path": str(file_path)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.post("/api/menu/analyze")
async def analyze_menu(file: UploadFile = File(...)):
    """
    Analyze menu image and return extracted food items with details
    This endpoint combines upload and analysis in one step
    """
    file_path = None

    try:
        # Validate file
        validate_image(file)

        # Generate unique filename
        import uuid
        file_ext = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename

        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()

            # Check file size
            if len(content) > settings.MAX_UPLOAD_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
                )

            await f.write(content)

        # Analyze with AI
        print(f"🔍 Analyzing menu image: {unique_filename}")
        analysis_result = await ai_service.analyze_menu_image(str(file_path))

        # Generate images for each food item using DALL-E 3 (parallel processing)
        cuisine_type = analysis_result.get("cuisine_type")
        menu_items = analysis_result.get("menu_items", [])

        if menu_items and settings.OPENAI_API_KEY:
            print(f"🎨 Generating images for {len(menu_items)} food items using DALL-E 3...")
            menu_items = await image_search_service.generate_multiple_food_images(
                menu_items,
                cuisine_type
            )
            analysis_result["menu_items"] = menu_items
        else:
            # No API key or no items - set placeholder
            for item in menu_items:
                item["image_url"] = None

        # TODO: Cross-reference with allergen database
        # TODO: Apply user preferences filter

        return {
            "success": True,
            "filename": unique_filename,
            "analysis": analysis_result
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    finally:
        # Optional: Clean up uploaded file after analysis
        # Uncomment if you don't want to keep uploaded files
        # if file_path and file_path.exists():
        #     file_path.unlink()
        pass


@app.get("/api/menu/items/{filename}")
async def get_menu_analysis(filename: str):
    """
    Retrieve previously analyzed menu by filename
    (Requires database implementation to store results)
    """
    # TODO: Implement database lookup
    raise HTTPException(status_code=501, detail="Not implemented yet - requires database")


@app.delete("/api/menu/items/{filename}")
async def delete_menu_image(filename: str):
    """Delete uploaded menu image"""
    try:
        file_path = UPLOAD_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        file_path.unlink()
        return {"message": "File deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


# User Profile Endpoints (to be implemented with database)
@app.post("/api/user/profile")
async def create_user_profile(db: Session = Depends(get_db)):
    """Create user profile with dietary preferences and allergies"""
    # TODO: Implement with database
    raise HTTPException(status_code=501, detail="Not implemented yet - requires database")


@app.get("/api/user/profile/{user_id}")
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Get user profile"""
    # TODO: Implement with database
    raise HTTPException(status_code=501, detail="Not implemented yet - requires database")


@app.put("/api/user/profile/{user_id}")
async def update_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Update user profile"""
    # TODO: Implement with database
    raise HTTPException(status_code=501, detail="Not implemented yet - requires database")


# Allergen Information Endpoint
@app.get("/api/allergens")
async def get_allergen_list():
    """Get list of common allergens"""
    allergens = [
        {"id": 1, "name": "Dairy", "description": "Milk and milk products"},
        {"id": 2, "name": "Eggs", "description": "Eggs and egg products"},
        {"id": 3, "name": "Nuts", "description": "Tree nuts (almonds, walnuts, cashews, etc.)"},
        {"id": 4, "name": "Peanuts", "description": "Peanuts and peanut products"},
        {"id": 5, "name": "Gluten", "description": "Wheat, barley, rye"},
        {"id": 6, "name": "Soy", "description": "Soybeans and soy products"},
        {"id": 7, "name": "Shellfish", "description": "Shrimp, crab, lobster, etc."},
        {"id": 8, "name": "Fish", "description": "Fish and fish products"},
        {"id": 9, "name": "Sesame", "description": "Sesame seeds and sesame oil"},
    ]
    return {"allergens": allergens}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
