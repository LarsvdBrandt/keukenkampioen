import os
import sys
from openai import OpenAI

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)

with open("index.html", "r") as f:
    current_html = f.read()

issue_title = os.environ.get("ISSUE_TITLE", "").strip()
issue_body = os.environ.get("ISSUE_BODY", "").strip()

prompt = issue_title
if issue_body:
    prompt += f"\n\n{issue_body}"

if not prompt:
    print("Geen prompt gevonden, stoppen.")
    sys.exit(0)

print(f"Prompt: {prompt[:100]}...")

response = client.chat.completions.create(
    model="gpt-4o",
    max_tokens=16000,
    messages=[
        {
            "role": "system",
            "content": "Je bent een web developer die de single-page HTML app 'Keuken Kampioen' onderhoudt. Geef altijd ALLEEN de volledige bijgewerkte index.html terug — geen uitleg, geen markdown code blocks, alleen pure HTML."
        },
        {
            "role": "user",
            "content": f"Huidige index.html:\n\n{current_html}\n\nAanpassing: {prompt}"
        }
    ]
)

new_html = response.choices[0].message.content.strip()

# Strip markdown code fences if present
if new_html.startswith("```html"):
    new_html = new_html[7:]
elif new_html.startswith("```"):
    new_html = new_html[3:]
if new_html.endswith("```"):
    new_html = new_html[:-3]
new_html = new_html.strip()

if not new_html.startswith("<!DOCTYPE") and not new_html.startswith("<"):
    print("Onverwachte response, stoppen.")
    print(new_html[:200])
    sys.exit(1)

with open("index.html", "w") as f:
    f.write(new_html)

print("index.html bijgewerkt.")
