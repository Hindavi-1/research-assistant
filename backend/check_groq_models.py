# check_groq_models.py
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise SystemExit("GROQ_API_KEY env var not set. Run: $env:GROQ_API_KEY = 'gsk_...'")

client = Groq(api_key=api_key)

print(f"{'MODEL ID':45s}  CONTEXT")
print("-" * 60)
for m in client.models.list().data:
    ctx = getattr(m, "context_window", "?")
    print(f"{m.id:45s}  {ctx}")