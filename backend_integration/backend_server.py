import json
import base64
import io
from flask import Flask, jsonify, request
import google.generativeai as genai
from PIL import Image

# Set up your API key
API_KEY = "PUT YOUR API HERE"
genai.configure(api_key=API_KEY)

# Initialize Flask
app = Flask(__name__)

@app.route("/describe_image", methods=["POST"])
def describe_image():
    data = request.get_json()
    image_base64 = data.get("image_base64")
    if not image_base64:
        return jsonify({"error": "No image provided"}), 400

    try:
        # Decode Base64 into an image
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
    except Exception as e:
        return jsonify({"error": "Invalid image data", "details": str(e)}), 400

    try:
        # Load the Gemini model
        model = genai.GenerativeModel("gemini-1.5-pro-latest")

        # ✅ Add a text prompt for the model
        response = model.generate_content(
            ["Describe this image in detail:", image]
        )

        # Extract the text response
        description = response.text if response else "No description found"
    except Exception as e:
        description = f"Error retrieving description from Gemini: {str(e)}"

    return jsonify({"description": description}), 200

if __name__ == "__main__":
    # Run the app on all available IP addresses (0.0.0.0) and port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
