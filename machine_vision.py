# https://platform.openai.com/docs/guides/vision#uploading-base64-encoded-images
import base64
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Path to your image
image_path = "path_to_your_image.png"

# Getting the base64 string
base64_image = encode_image(image_path)

response = openai.ChatCompletion.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "system",
      "content": "You are a helpful assistant specialized in interpreting visual content."
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          # "text": "What is in this image?",
          "text": "Can you provide insights about this image?",
        },
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
)

print(response.choices[0])
