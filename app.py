from flask import Flask, request, send_file, jsonify
from io import BytesIO
import os
import createFontImage

app = Flask(__name__)

@app.route('/generate-font-image', methods=['POST'])
def generate_image():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        if not data or 'font_id' not in data:
            return jsonify({"error": "Missing 'font_id' in request body"}), 400
        
        font_id = data['font_id']

        # Define the base fonts directory
        fonts_directory = "fonts"

        # Construct the path to the font folder
        font_folder_path = os.path.join(fonts_directory, font_id)

        # Check if the folder exists
        if not os.path.isdir(font_folder_path):
            return jsonify({"error": "Invalid 'font_id' "}), 400

        # Find the .ttf file in the folder
        ttf_files = [f for f in os.listdir(font_folder_path) if f.endswith('.ttf')]
        if not ttf_files:
            return jsonify({"error": "No font file found for this id"}), 400

        # Use the first .ttf file found
        font_path = os.path.join(font_folder_path, ttf_files[0])

        # Get the text and text color from the request data
        text = data.get('text', '')
        text_color = data.get('text_color', '#000000')
        
        # Convert hex color to RGB tuple
        text_color = tuple(int(text_color[i:i+2], 16) for i in (1, 3, 5))

        # Define image size (you can adjust this as needed)
        image_size = (500, 500)

        # Create the image using the provided function
        img = createFontImage.create_text_image(text, font_path, image_size, text_color)

        # Save the image to a BytesIO object
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Send the image as a response
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
     port = int(os.environ.get("PORT", 5000))
     app.run(debug=True, host='0.0.0.0', port=port)
