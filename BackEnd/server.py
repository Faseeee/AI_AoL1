# ... (your existing Python code: imports, NUTRITION_DB, classify_image, etc. go here) ...
# ... (make sure your image path is removed or commented out for now: img_path=r"test2.jpeg") ...


# ----------------------------------------------------
# FLASK SERVER CODE to expose your functions as an API
# ----------------------------------------------------
from flask import Flask, request, jsonify
import base64
import io

app = Flask(__name__)

@app.route('/analyze_meal', methods=['POST'])
def analyze_meal():
    # 1. Get Image Data from Flutter Request
    try:
        data = request.json
        # The image is sent as a base64 encoded string from Flutter
        image_base64 = data['image_base64']
        image_bytes = base64.b64decode(image_base64)
        
        # Save bytes to a temporary file-like object for PIL/Keras to read
        img_temp = io.BytesIO(image_bytes)
        temp_file_path = "temp_meal_image.jpg" # Required for Keras model loading, as it expects a path
        with open(temp_file_path, 'wb') as f:
            f.write(image_bytes)
            
    except Exception as e:
        return jsonify({"error": "Invalid image or request format.", "details": str(e)}), 400

    # 2. Run Keras Classification
    food_type = classify_image(temp_file_path)
    
    if food_type == "unknown_food":
        os.remove(temp_file_path) # Clean up temp file
        return jsonify({
            "success": False,
            "message": "Classification failed. Unknown food category.",
        }), 200

    # 3. Run Gemini Portion Estimation
    qty, raw_text, used_default = estimate_portion_size_gemini(temp_file_path, food_type)
    
    # 4. Calculate Nutrition
    nutrition_result_text = calculate_nutrition(food_type, qty, used_default)

    # Clean up temp file
    os.remove(temp_file_path)

    # 5. Return Results to Flutter
    return jsonify({
        "success": True,
        "food_type": food_type.replace('_', ' ').title(),
        "nutrition_summary": nutrition_result_text,
        "portion_raw_response": raw_text,
        "quantity": qty,
        "is_default_used": used_default,
    }), 200

if __name__ == '__main__':
    # Flask server runs on http://127.0.0.1:5000/
    print("Starting Flask Server on http://127.0.0.1:5000/")
    # Use 0.0.0.0 if running on a separate machine/network, otherwise 127.0.0.1 is fine for local testing
    app.run(debug=True, host='127.0.0.1', port=5000)