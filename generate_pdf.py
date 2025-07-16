import os
import re
import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def render_persona_pdf(username, persona_text, avatar_path=None, posts=None, comments=None):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("persona_template.html")

    section_header_pattern = re.compile(r"^\*\*(\d+)\.\s*(.+?):\*\*$")
    sections_dict = {}
    current_key = None
    current_value = []

    for line in persona_text.splitlines():
        line = line.strip()
        if not line:
            continue
        match = section_header_pattern.match(line)
        if match:
            if current_key:
                sections_dict[current_key] = "\n".join(current_value)
            current_key = match.group(2).strip()
            current_value = []
        elif current_key:
            current_value.append(line)

    if current_key:
        sections_dict[current_key] = "\n".join(current_value)

    demographics = {}
    if "Demographics (Hypothetical)" in sections_dict:
        for line in sections_dict["Demographics (Hypothetical)"].splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                demographics[key.strip()] = value.strip()

    # Parse personality traits into structured data for progress bars
    personality_traits = []
    personality_text = sections_dict.get("Personality", "")
    if personality_text:
        # Extract key personality traits and assign mock values for visualization
        traits = ["Curious", "Analytical", "Tech-savvy", "Introspective", "Socially aware"]
        values = [85, 90, 95, 75, 80]  # Mock percentage values
        for trait, value in zip(traits, values):
            if trait.lower() in personality_text.lower():
                personality_traits.append({"label": trait, "value": value})

    # Parse tech savviness into numeric value
    tech_savviness_text = sections_dict.get("Tech Savviness", "")
    tech_savviness_value = 50  # Default value
    if "high" in tech_savviness_text.lower():
        tech_savviness_value = 85
    elif "medium" in tech_savviness_text.lower():
        tech_savviness_value = 65
    elif "low" in tech_savviness_text.lower():
        tech_savviness_value = 35

    context = {
        "username": username,
        "avatar_path": f"file:///{os.path.abspath(avatar_path).replace(os.sep, '/')}" if avatar_path else None,
        "demographics": demographics,
        "interests": sections_dict.get("Interests", ""),
        "tone": sections_dict.get("Tone", ""),
        "opinions": sections_dict.get("Opinions", ""),
        "hobbies": sections_dict.get("Hobbies & Behaviors", ""),
        "personality": personality_traits,
        "values": sections_dict.get("Values", ""),
        "tech_savviness": tech_savviness_value,
        "motivations": sections_dict.get("Motivations", ""),
        "posts": posts if posts else [],
        "comments": comments if comments else [],
        "suggested_picture": sections_dict.get("\U0001f5bc️ Suggested Profile Picture", ""),
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    html = template.render(**context)

    os.makedirs("persona_outputs", exist_ok=True)
    output_pdf = f"persona_outputs/{username}_persona.pdf"
    wkhtmltopdf_path = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    if not os.path.exists(wkhtmltopdf_path):
        raise FileNotFoundError(f"wkhtmltopdf not found at {wkhtmltopdf_path}. Please install it or update the path.")
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    try:
        pdfkit.from_string(html, output_pdf, configuration=config, options={"enable-local-file-access": ""})
        print(f"[✓] PDF saved to {output_pdf}")
        return output_pdf
    except Exception as e:
        print(f"[✗] Failed to generate PDF: {e}")
        return None

if __name__ == "__main__":
    with open("persona_outputs/kojied_persona.txt", "r", encoding="utf-8") as f:
        persona_text = f.read()
    render_persona_pdf("kojied", persona_text, avatar_path="persona_outputs/kojied_avatar.png")
