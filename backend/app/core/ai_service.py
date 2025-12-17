"""
AI Service for menu image analysis using OpenAI or Anthropic APIs
"""
import base64
import os
from typing import Dict, List, Optional
from pathlib import Path
import anthropic
from openai import OpenAI
from app.core.config import settings


class AIService:
    """Service for AI-powered menu analysis"""

    def __init__(self):
        self.provider = settings.AI_PROVIDER.lower()
        if self.provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        elif self.provider == "openai":
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            raise ValueError(f"Unsupported AI provider: {settings.AI_PROVIDER}")

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _get_image_media_type(self, image_path: str) -> str:
        """Get media type from image file extension"""
        ext = Path(image_path).suffix.lower()
        media_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".gif": "image/gif"
        }
        return media_types.get(ext, "image/jpeg")

    async def analyze_menu_image(self, image_path: str) -> Dict:
        """
        Analyze menu image and extract food items with details

        Args:
            image_path: Path to the menu image file

        Returns:
            Dictionary containing analysis results with menu items
        """
        if self.provider == "anthropic":
            return await self._analyze_with_anthropic(image_path)
        else:
            return await self._analyze_with_openai(image_path)

    async def _analyze_with_anthropic(self, image_path: str) -> Dict:
        """Analyze menu using Anthropic Claude"""
        image_data = self._encode_image(image_path)
        media_type = self._get_image_media_type(image_path)

        prompt = """Analyze this restaurant menu image and extract detailed information about each food item.

For each dish you identify, provide:
1. **Name**: The exact name of the dish as written on the menu
2. **Food Type**: Classify as one of: Vegetarian, Non-Vegetarian, Vegan, or Unknown
3. **Meat Type**: If non-vegetarian, specify the meat (e.g., Chicken, Beef, Pork, Fish, Lamb, Seafood, etc.). Mark clearly if it contains pork or beef.
4. **Ingredients**: List the main ingredients you can identify or infer
5. **Common Allergens**: Identify potential allergens from this list: Dairy, Eggs, Nuts, Peanuts, Gluten, Soy, Shellfish, Fish, Sesame

Please return your response in this exact JSON format:
{
  "menu_items": [
    {
      "name": "Dish name",
      "food_type": "Vegetarian|Non-Vegetarian|Vegan|Unknown",
      "meat_type": "Chicken|Beef|Pork|Fish|Lamb|Seafood|None",
      "contains_pork": false,
      "contains_beef": false,
      "ingredients": ["ingredient1", "ingredient2"],
      "allergens": ["Dairy", "Gluten"]
    }
  ],
  "cuisine_type": "Type of cuisine if identifiable",
  "language": "Language of the menu"
}

Be thorough and analyze all visible items on the menu."""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )

            # Extract the text content
            response_text = message.content[0].text

            # Parse JSON from response
            import json
            # Try to extract JSON from the response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            result = json.loads(response_text)
            return result

        except Exception as e:
            print(f"Error analyzing with Anthropic: {str(e)}")
            raise

    async def _analyze_with_openai(self, image_path: str) -> Dict:
        """Analyze menu using OpenAI GPT-4 Vision"""
        image_data = self._encode_image(image_path)

        prompt = """Analyze this restaurant menu image and extract detailed information about each food item.

For each dish you identify, provide:
1. **Name**: The exact name of the dish as written on the menu
2. **Food Type**: Classify as one of: Vegetarian, Non-Vegetarian, Vegan, or Unknown
3. **Meat Type**: If non-vegetarian, specify the meat (e.g., Chicken, Beef, Pork, Fish, Lamb, Seafood, etc.). Mark clearly if it contains pork or beef.
4. **Ingredients**: List the main ingredients you can identify or infer
5. **Common Allergens**: Identify potential allergens from this list: Dairy, Eggs, Nuts, Peanuts, Gluten, Soy, Shellfish, Fish, Sesame

Please return your response in this exact JSON format:
{
  "menu_items": [
    {
      "name": "Dish name",
      "food_type": "Vegetarian|Non-Vegetarian|Vegan|Unknown",
      "meat_type": "Chicken|Beef|Pork|Fish|Lamb|Seafood|None",
      "contains_pork": false,
      "contains_beef": false,
      "ingredients": ["ingredient1", "ingredient2"],
      "allergens": ["Dairy", "Gluten"]
    }
  ],
  "cuisine_type": "Type of cuisine if identifiable",
  "language": "Language of the menu"
}

Be thorough and analyze all visible items on the menu."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4000
            )

            response_text = response.choices[0].message.content

            # Parse JSON from response
            import json
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            result = json.loads(response_text)
            return result

        except Exception as e:
            print(f"Error analyzing with OpenAI: {str(e)}")
            raise


# Global AI service instance
ai_service = AIService()
