import anthropic
import os
import sys

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

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

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    messages=[
        {
            "role": "user",
            "content": f"""Je bent een web developer die de single-page HTML app "Keuken Kampioen" onderhoudt.

Hier is de huidige index.html:

<current_html>
{current_html}
</current_html>

Pas de volgende aanpassing toe:

{prompt}

Geef ALLEEN de volledige bijgewerkte index.html terug. Geen uitleg, geen markdown code blocks, geen andere tekst — alleen de pure HTML."""
        }
    ]
)

new_html = message.content[0].text.strip()

# Strip markdown code fences if present
if new_html.startswith("```html"):
    new_html = new_html[7:]
elif new_html.startswith("```"):
    new_html = new_html[3:]
if new_html.endswith("```"):
    new_html = new_html[:-3]
new_html = new_html.strip()

if not new_html.startswith("<!DOCTYPE") and not new_html.startswith("<"):
    print("Onverwachte response van Claude, stoppen.")
    print(new_html[:200])
    sys.exit(1)

with open("index.html", "w") as f:
    f.write(new_html)

print("index.html bijgewerkt.")
