import os
from urllib.parse import urlparse
from scrape_reddit import get_user_content
from generate_persona import generate_user_persona

def extract_username(url):
    return urlparse(url).path.split('/')[2]

def save_to_file(username, persona):
    os.makedirs("persona_outputs", exist_ok=True)
    with open(f"persona_outputs/{username}_persona.txt", "w", encoding='utf-8') as f:
        f.write(persona)

def main(url):
    username = extract_username(url)
    print(f"[+] Scraping Reddit user: {username}")
    posts, comments = get_user_content(username)
    print("[+] POSTS:")
    for i, p in enumerate(posts): print(f"{i+1}. {p}")

    print("\n[+] COMMENTS:")
    for i, c in enumerate(comments): print(f"{i+1}. {c}")

    print(f"[+] Generating persona via Gemini...")
    persona = generate_user_persona(posts, comments, username)

    save_to_file(username, persona)
    print(f"[✓] Persona saved to persona_outputs/{username}_persona.txt")

if __name__ == "__main__":
    reddit_urls = [
        "https://www.reddit.com/user/kojied/",
        "https://www.reddit.com/user/Hungry-Move-6603/",
        "https://www.reddit.com/user/GallowBoob/",
        "https://www.reddit.com/user/Unidan/",
        "https://www.reddit.com/user/spez/",
        "https://www.reddit.com/user/Shitty_Watercolour/",
    ]
    for url in reddit_urls:
        main(url)