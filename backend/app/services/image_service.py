import os
import asyncio
from huggingface_hub import AsyncInferenceClient
from app.services.supabase_client import get_supabase_client
from typing import Optional

class ImageService:
    def __init__(self):
        # Use HuggingFace Inference API (Free tier supports basic generation)
        # Recommended Model: stabilityai/stable-diffusion-xl-base-1.0 or appropriate fast model
        self.api_key = os.getenv("HF_TOKEN")
        self.client = AsyncInferenceClient(token=self.api_key)
        self.supabase = get_supabase_client()
        # SDXL is large, might hit timeouts on free tier. 
        # 'runwayml/stable-diffusion-v1-5' or 'stabilityai/stable-diffusion-2-1' might be safer for free inference.
        # Let's try SD-2-1 for better quality than v1.5
        self.model_id = "stabilityai/stable-diffusion-2-1" 

    async def generate_scene_image(self, prompt: str, scene_id: str) -> Optional[str]:
        """
        Generates an image for a scene and uploads it to Supabase Storage (bucket).
        Returns the public URL of the generated image.
        """
        try:
            # 1. Generate Image
            # The API returns a PIL Image object
            image = await self.client.text_to_image(prompt, model=self.model_id)
            
            # 2. Save to temporary buffer
            import io
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()

            # 3. Upload to Cloud Storage (Supabase Storage)
            # Define file path: scenes/{scene_id}_{timestamp}.png
            filename = f"scenes/{scene_id}_{os.urandom(4).hex()}.png"
            
            # Upload
            # Note: You need to create a bucket named 'images' in Supabase beforehand
            try:
                self.supabase.storage.from_("images").upload(
                    path=filename,
                    file=image_bytes,
                    file_options={"content-type": "image/png"}
                )
                
                # Get Public URL
                public_url_response = self.supabase.storage.from_("images").get_public_url(filename)
                # supabase-py v2 returns a string directly or a response? 
                # According to recent docs, get_public_url returns a string URL.
                return public_url_response

            except Exception as e:
                print(f"Storage upload failed: {e}")
                # Fallback: Can't return URL if storage fails.
                return None

        except Exception as e:
            print(f"Image generation failed: {e}")
            return None
