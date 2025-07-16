import os
import requests
import dotenv
from datetime import datetime
import re
from google import generativeai as genai
from generate_pdf import render_persona_pdf

dotenv.load_dotenv()

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in your .env file")

# Load image generation API token
IMAGE_API_KEY = os.getenv("IMAGE_API_KEY")
IMAGE_API_URL = "https://api.claid.ai/v1-beta1/image/generate"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)


def generate_image_from_description(prompt, username):
    headers = {
        "Authorization": f"Bearer {IMAGE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "*/*"
    }

    payload = {
        "input": prompt,
        "options": {
            "number_of_images": 1,
            "guidance_scale": 7
        }
    }

    response = requests.post(IMAGE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        output = data.get("data", {}).get("output", [])
        if output and "tmp_url" in output[0]:
            image_url = output[0]["tmp_url"]
        print(f"[✓] Image URL: {image_url}")

        img_data = requests.get(image_url).content
        os.makedirs("persona_outputs", exist_ok=True)
        path = f"persona_outputs/{username}_avatar.png"
        with open(path, "wb") as f:
            f.write(img_data)

        print(f"[✓] Image saved to: {path}")
        return path
    else:
        print(f"[✗] Failed to generate image: {response.status_code} - {response.text}")
        return None


def generate_user_persona(posts, comments, username):
    model = genai.GenerativeModel("gemini-1.5-flash")

    tagged_content = ""
    for i, p in enumerate(posts): tagged_content += f"[Post {i+1}] {p}\n"
    for i, c in enumerate(comments): tagged_content += f"[Comment {i+1}] {c}\n"

    prompt = f"""
You are an expert at building qualitative user personas.

From the following Reddit posts and comments, create a structured user persona with the following sections:
Username: {username}
1. Demographics (Hypothetical)
2. Interests
3. Tone
4. Opinions
5. Hobbies & Behaviors
6. Personality 
7. Values
8. Tech Savviness
9. Motivations
all sections should be concise, relevant, and based on the user's online presence and all sections are compulsory.
For each, cite relevant [Post X] or [Comment Y] entries used for inference.
Finally, give a profile picture description starting with:
🖼️ Suggested Profile Picture:

---
{tagged_content}
"""

    print("[+] Generating user persona via Gemini...")
    response = model.generate_content(prompt)
    persona_text = response.text

    # Save text persona
    os.makedirs("persona_outputs", exist_ok=True)
    with open(f"persona_outputs/{username}_persona.txt", "w", encoding="utf-8") as f:
        f.write(persona_text)

    # Extract image description
    match = re.search(r"🖼️ Suggested Profile Picture:\s*(.+)", persona_text, re.DOTALL)
    if match:
        img_description = match.group(1).strip()
        if len(img_description) > 1024:
            img_description = img_description[:1020] + "..."
        print(f"[+] Image prompt: {img_description}")
        image_path = generate_image_from_description(img_description, username)
    else:
        print("[!] No image prompt found.")
    render_persona_pdf(username, persona_text, avatar_path=image_path, posts=posts, comments=comments)

    return persona_text
