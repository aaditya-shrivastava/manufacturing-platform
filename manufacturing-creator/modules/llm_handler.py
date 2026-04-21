from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are a manufacturing expert. When given a manufacturing concept, respond in this exact format:

**Description**
Write 2-3 sentences describing what the product/concept is and what it does.

**Materials**
List 3-5 key materials used, each with a one-line explanation of why it's used.

Keep it concise and professional."""


def generate_narrative(user_prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=config.LLM_MODEL,
            max_tokens=config.MAX_TOKENS,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Generate a concept overview for: {user_prompt}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"LLM API error: {str(e)}")


def generate_image_prompt(user_prompt: str, narrative: str) -> str:
    try:
        response = client.chat.completions.create(
            model=config.LLM_MODEL,
            max_tokens=200,
            messages=[
                {"role": "system", "content": "Write concise, vivid DALL·E image prompts focused on visual details."},
                {"role": "user",   "content": (
                    f"Write a DALL·E prompt (max 150 words) for: '{user_prompt}'\n"
                    f"Context: {narrative[:400]}\n"
                    "Focus on photorealistic appearance, materials, factory/lab setting, professional lighting."
                )}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Image prompt generation error: {str(e)}")