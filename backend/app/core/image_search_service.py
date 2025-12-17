"""
Image Generation Service using DALL-E 3
Generates high-quality food images based on dish names
"""
import asyncio
from typing import Optional, Dict, List
from openai import OpenAI
from app.core.config import settings


class ImageSearchService:
    """Service for generating food images using DALL-E 3"""

    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def _generate_dalle_prompt(self, food_name: str, cuisine_type: Optional[str] = None) -> str:
        """
        Generate optimized DALL-E prompt for food photography

        Args:
            food_name: Name of the dish
            cuisine_type: Optional cuisine type

        Returns:
            Optimized prompt for DALL-E
        """
        # Build descriptive prompt for high-quality food photography
        cuisine_prefix = f"{cuisine_type} " if cuisine_type else ""

        prompt = (
            f"Professional food photography of {cuisine_prefix}{food_name}, "
            f"appetizing plated dish, overhead view, natural lighting, "
            f"beautiful presentation on white ceramic plate, "
            f"restaurant quality, high resolution, photorealistic, "
            f"no text, no watermark, clean background"
        )

        return prompt

    async def generate_food_image(self, food_name: str, cuisine_type: Optional[str] = None) -> Optional[str]:
        """
        Generate a high-quality food image using DALL-E 3

        Args:
            food_name: Name of the food/dish
            cuisine_type: Optional cuisine type for better results

        Returns:
            URL of the generated image, or None if generation failed
        """
        if not settings.OPENAI_API_KEY:
            print("⚠️  OpenAI API key not configured")
            return None

        try:
            # Generate DALL-E prompt
            prompt = self._generate_dalle_prompt(food_name, cuisine_type)

            print(f"🎨 Generating image for: {food_name}")

            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",  # Use "hd" for higher quality but slower
                    n=1,
                )
            )

            # Extract image URL from response
            if response.data and len(response.data) > 0:
                image_url = response.data[0].url
                print(f"✅ Generated image for: {food_name}")
                return image_url
            else:
                print(f"⚠️  No image generated for: {food_name}")
                return None

        except Exception as e:
            print(f"❌ Image generation error for '{food_name}': {str(e)}")
            return None

    async def generate_multiple_food_images(
        self,
        food_items: List[Dict],
        cuisine_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Generate images for multiple food items in parallel

        Args:
            food_items: List of food item dictionaries with 'name' key
            cuisine_type: Optional cuisine type for better results

        Returns:
            List of food items with added 'image_url' field
        """
        print(f"🚀 Starting parallel image generation for {len(food_items)} items...")

        # Create tasks for parallel processing
        tasks = []
        for item in food_items:
            food_name = item.get("name", "")
            if food_name:
                task = self.generate_food_image(food_name, cuisine_type)
                tasks.append(task)
            else:
                tasks.append(asyncio.sleep(0))  # Placeholder for empty names

        # Execute all tasks in parallel
        image_urls = await asyncio.gather(*tasks, return_exceptions=True)

        # Assign generated URLs to items
        for i, item in enumerate(food_items):
            if i < len(image_urls):
                result = image_urls[i]
                if isinstance(result, str):
                    item["image_url"] = result
                elif isinstance(result, Exception):
                    print(f"⚠️  Exception for {item.get('name')}: {result}")
                    item["image_url"] = None
                else:
                    item["image_url"] = None
            else:
                item["image_url"] = None

        print(f"✅ Completed parallel image generation")
        return food_items


# Global image search service instance
image_search_service = ImageSearchService()
