from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

if os.environ.get('OPENAI_API_KEY'):
    client = OpenAI()

async def generate_tone_sentiment(text: str, stars: int):
    if os.environ.get('OPENAI_API_KEY'):
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Analyze the tone of the following review (stars: {stars}): {text}. Respond with only the predicted tone.",
            max_tokens=60
        )

        tone = response.choices[0].text.strip()

        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Analyze the sentiment of the following review, [either positive, negative or neutral]. (stars: {stars}): {text}. Respond with only the predicted sentiment.",
            max_tokens=60
        )
        sentiment = response.choices[0].text.strip()
    else:
        tone, sentiment = 'N/A', 'N/A'
    
    return tone, sentiment
 