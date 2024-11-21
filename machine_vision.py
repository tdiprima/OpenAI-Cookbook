# Combining Machine Vision to Analyze and Describe Images Dynamically
# TODO: Doesn't work; need correct model.
# https://platform.openai.com/docs/guides/vision
import os
import openai

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to upload image and get description
def describe_image(m_image_path):
    with open(m_image_path, "rb") as image_file:
        response = openai.Image.create_edit(
            image=image_file,  # Pass image file
            prompt="Describe this image in detail.",
            size="1024x1024"
        )
    return response


# Function to interpret description using GPT
def interpret_image_description(description):
    response = openai.ChatCompletion.create(
        model="gpt-4-vision",  # gpt-4o-mini gpt-4-vision-preview gpt-4o???
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in interpreting visual content."},
            {"role": "user", "content": f"Can you provide insights about this image? {description}"}
        ]
    )
    return response['choices'][0]['message']['content']


# Main execution
image_path = "path_to_your_image.png"  # Uploaded image must be a PNG and less than 4 MB
image_description = describe_image(image_path)
interpretation = interpret_image_description(image_description)

print("Image Description:", image_description)
print("Interpretation:", interpretation)
