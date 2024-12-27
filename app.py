from flask import Flask, json, request, send_file, jsonify
from io import BytesIO
import os
import createFontImage

app = Flask(__name__)
@app.route('/tutorial-image-links', methods=['POST'])
def get_links_for_unity():
    print("Request received")
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "Invalid JSON data"}), 400
    # Extract tutorial-id and type from the request
        tutorial_id = request_data.get('tutorial-id')
        if not tutorial_id:
            return jsonify({"error": "Missing 'tutorial-id' in request body"}), 400
        

        if tutorial_id[0].isdigit():
           with open('steps_data.json', 'r') as file:
                data = json.load(file)
        else:
            with open('advanced_steps_data.json', 'r') as file:
                data = json.load(file)
            

    # Search for the tutorial-id and type in the data
        for tutorial in data:
            if tutorial['tutorial-id'] == tutorial_id:
                    return jsonify({
                        "steps": len(tutorial['tutorial'])-1,
                        "images": tutorial['tutorial']
                    })
        
        return jsonify({'error': 'Tutorial not found'}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/font-image', methods=['POST'])
def generate_image():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        if not data or 'font-id' not in data:
            return jsonify({"error": "Missing 'font_id' in request body"}), 400
        
        # Extract the font_id from the request
        font_id, text, text_color = data['font-id'].split('-||-')

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
     app.run(debug=True, host='127.0.0.1', port=port)

