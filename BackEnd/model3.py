import os
import re
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.preprocessing import image
from google import genai


API_KEY = "AIzaSyBWrfG3_iozt18C-aqs3fJoyzYmLkdCQL8" 

try:

    client = genai.Client(api_key=API_KEY)
    GEMINI_MODEL = 'gemini-2.5-flash'
    print("Gemini client initialized successfully.")
except Exception as e:
    print("Error initializing Gemini client. The API key might be invalid or there's a connection issue.")
    print(f"Details: {e}")
    client = None
    GEMINI_MODEL = None

categories = ["chicken_wings","donuts","dumplings","french_fries","fried_rice","hamburger","ice_cream","pizza","steak"]
NUTRITION_DB = {
    "chicken_wings": {
        "unit": "piece", "default_count": 4, 
        "cal": 90, "prot": 8, "carb": 0, "fat": 6  # Per 1 piece
    },
    "donuts": {
        "unit": "piece", "default_count": 1, 
        "cal": 250, "prot": 3, "carb": 30, "fat": 13 # Per 1 donut
    },
    "dumplings": {
        "unit": "piece", "default_count": 6, 
        "cal": 40, "prot": 2, "carb": 5, "fat": 1   # Per 1 dumpling
    },
    "french_fries": {
        "unit": "serving", "default_count": 1, 
        "cal": 365, "prot": 4, "carb": 48, "fat": 17 # Per Medium serving
    },
    "fried_rice": {
        "unit": "serving", "default_count": 1, 
        "cal": 400, "prot": 12, "carb": 55, "fat": 15 
    },
    "hamburger": {
        "unit": "piece", "default_count": 1, 
        "cal": 500, "prot": 25, "carb": 40, "fat": 28 
    },
    "ice_cream": {
        "unit": "scoop", "default_count": 2, 
        "cal": 137, "prot": 2, "carb": 16, "fat": 7 # Per scoop
    },
    "pizza": {
        "unit": "slice", "default_count": 2, 
        "cal": 285, "prot": 12, "carb": 36, "fat": 10 # Per slice
    },
    "steak": {
        "unit": "serving", "default_count": 1, 
        "cal": 600, "prot": 50, "carb": 0, "fat": 40 # Per steak
    }
}

modelSavedPath = r"I:\My Drive\Binus\Semester 3\Artificial Intelligence\datasetfood\dataset_for_model\foodV3.keras"

def classify_image(imageFile):
    """
    Loads the Keras model and classifies the food in the image.
    This function uses your original logic.
    """
    try:
        model = tf.keras.models.load_model(modelSavedPath)

        img = Image.open(imageFile)
        img.load()
        img = img.resize((320, 320), Image.LANCZOS) 

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)


        pred = model.predict(x, verbose=0)
        categoryValue = np.argmax(pred, axis=1)[0]
        
        result = categories[categoryValue]
        return result

    except FileNotFoundError:
        print(f"Error: Image or model file not found.")
        return "unknown_food"
    except Exception as e:
        print(f"Error in Keras classification: {e}")
        return "unknown_food"

def estimate_portion_size_gemini(imageFile, food_category):
    """
    Uses the Gemini model to estimate the portion size using a multimodal prompt.
    Returns: (multiplier, raw_text, is_default_used)
    """
    # Helper to get default value safely
    def get_default():
        if food_category in NUTRITION_DB:
            return NUTRITION_DB[food_category]["default_count"]
        return 1  # Fallback if category totally missing

    # 1. Handle Unknown Category immediately
    if food_category == "unknown_food":
        return 1, "Unknown food category", True

    try:
        img = Image.open(imageFile)
        
        # Added spaces at end of lines so sentences don't merge
        prompt = (
            f"Analyze the portion of **{food_category}** in the image. "
            "Estimate the serving size (small, medium, or large) relative to a standard adult serving. "
            "Count the number of pieces (if applicable, like slices or wings). "
            "Provide the number of pieces only or the portion size if uncountable. "
            "If you provided the number do not provide the portion size. "
            "The answer should be either be a number or portion size."
        )
        
        response = client.models.generate_content(
            model=GEMINI_MODEL,  # Make sure this variable name matches your setup (e.g. GEMINI_MODEL or GEMINI_MODEL_ID)
            contents=[prompt, img]
        )
        
        text = response.text.strip().lower()
        
        # Logic to parse Gemini's text result into a number
        multiplier = 1.0
        
        # Check for keywords
        if "small" in text:
            multiplier = 0.75
        elif "large" in text:
            multiplier = 1.5
        elif "medium" in text:
            multiplier = 1.0
        else:
            # Try to find a number in the text (e.g., "3" or "2.5")
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
            if numbers:
                multiplier = float(numbers[0])
            else:
                # Parsing failed -> Return 3 values (Default, Text, True)
                return get_default(), text, True 

        # Success -> Return 3 values (Calculated, Text, False)
        return multiplier, text, False

    except FileNotFoundError:
        # File Error -> Return 3 values
        return get_default(), f"Error: Image not found at {imageFile}", True
        
    except Exception as e:
        # API Error -> Return 3 values
        return get_default(), f"API Error: {e}", True

def calculate_nutrition(category, quantity, is_default):
    data = NUTRITION_DB.get(category)
    if not data:
        return "No data for this category."

    # If the database unit is "serving", quantity is a multiplier (e.g. 1.5x serving)
    # If the database unit is "piece", quantity is the count (e.g. 3 pieces)
    # In both cases, simple multiplication works effectively here.
    
    total_cal = data["cal"] * quantity
    total_prot = data["prot"] * quantity
    total_carb = data["carb"] * quantity
    total_fat = data["fat"] * quantity

    status_msg = "(Estimated by AI)"
    if is_default:
        status_msg = "(⚠ Portion not detected - Using Default)"

    result = (
        f"--- NUTRITION FACTS ---\n"
        f"Food: {category.replace('_', ' ').title()}\n"
        f"Portion: {quantity} {data['unit']}(s) {status_msg}\n"
        f"-----------------------\n"
        f"Calories: {total_cal:.0f} kcal\n"
        f"Protein:  {total_prot:.1f} g\n"
        f"Carbs:    {total_carb:.1f} g\n"
        f"Fat:      {total_fat:.1f} g\n"
    )
    return result

img_path=r"test2.jpeg" 

print(f"--- 1. Running Keras Classification for: {img_path} ---")
food_type = classify_image(img_path)
print(f"Classification Result: **{food_type}**")

print("\n--- 2. Running Gemini for Portion Size Estimation ---")
qty, raw_text, used_default = estimate_portion_size_gemini(img_path, food_type)
print(f"Portion Analysis: \n{qty}")

print("\n--- Combined Result ---")
print(f"Food Type: {food_type}")
print(f"Portion Estimate: {raw_text}")
if food_type in NUTRITION_DB:
    # Step 2: Get Portion
    print("Analyzing portion size...")
    # qty, raw_text, used_default = get_portion_multiplier(test_img, food_type)
        
    # Step 3: Calculate & Print
    print("\n" + calculate_nutrition(food_type, qty, used_default))
    #print(f"Debug Info -> Raw AI Response: '{raw_text}'")
else:
    print("Unknown food category. Cannot calculate nutrition.")