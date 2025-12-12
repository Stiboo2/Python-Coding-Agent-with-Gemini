import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=api_key) 
response = gemini_client.models.generate_content(
     model="gemini-2.5-flash",
     contents="What is the capital of France?"
)
print(response.text)     


# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# google_api_key = os.getenv("GEMINI_API_KEY")

# # Gemini-compatible OpenAI endpoint
# gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

# # Create Gemini client using OpenAI SDK
# gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)

# system_message = "You are a helpful assistant"

# def message_gpt(prompt):
#     messages = [
#         {"role": "system", "content": system_message},
#         {"role": "user", "content": prompt}
#     ]

#     response = gemini.chat.completions.create(
#         model="gemini-2.5-pro",
#         messages=messages
#     )

#     return response.choices[0].message.content


# # ---- Example usage ----
# result = message_gpt("What is the capital of France?")
# print(result)
#  """