import requests
import os
from openai import OpenAI
from datetime import datetime
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)


def generate_image(image_prompt: str, save_locally: bool = True) -> dict:
    """
    Generates an image using DALL·E 3 from a given prompt.

    Args:
        image_prompt: The visual description prompt for DALL·E
        save_locally: Whether to save the image to disk

    Returns:
        dict with keys: 'url', 'local_path' (if saved), 'revised_prompt'
    """
    try:
        response = client.images.generate(
            model=config.IMAGE_MODEL,
            prompt=image_prompt,
            size=config.IMAGE_SIZE,
            quality=config.IMAGE_QUALITY,
            n=1
        )

        image_url      = response.data[0].url
        revised_prompt = response.data[0].revised_prompt  # DALL·E may adjust your prompt

        result = {
            "url": image_url,
            "revised_prompt": revised_prompt,
            "local_path": None
        }

        # Optionally download and save the image
        if save_locally:
            local_path = _save_image(image_url)
            result["local_path"] = local_path

        return result

    except Exception as e:
        raise RuntimeError(f"Image generation error: {str(e)}")


def _save_image(image_url: str) -> str:
    """
    Downloads and saves an image from a URL to the local data folder.

    Args:
        image_url: URL of the generated image

    Returns:
        Local file path where the image was saved
    """
    save_dir = "./data/stored_concepts"
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"concept_{timestamp}.png"
    filepath  = os.path.join(save_dir, filename)

    img_data = requests.get(image_url, timeout=30).content
    with open(filepath, "wb") as f:
        f.write(img_data)

    return filepath
