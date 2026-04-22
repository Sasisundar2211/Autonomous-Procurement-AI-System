import os

from openai import OpenAI


def generate_explanation(top_vendor: str, row) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Top vendor selected based on strongest weighted score across cost, delivery, quality, and defect performance."

    client = OpenAI(api_key=api_key)
    prompt = f"""
Explain why vendor {top_vendor} is selected.
Data: {row.to_dict()}
Keep it short and business-focused.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a procurement analyst. Reply in 1-2 concise business sentences.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=120,
    )

    content = response.choices[0].message.content or ""
    return " ".join(content.split())
