import cv2
import numpy as np
from keras.applications import Xception  # Import Xception model
import requests

# Load the pre-trained Xception model
model = Xception(weights='imagenet', include_top=False)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (299, 299))  # XceptionNet input size
    img = img.astype('float32') / 255.0  # Normalize to 0-1
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def analyze_media(images):
    results = {}

    for image_url in images:
        try:
            image = download_image(image_url)
            if image is None:
                results[image_url] = "Image could not be downloaded"
                continue
            
            preprocessed_img = preprocess_image(image)
            prediction = model.predict(preprocessed_img)

            if prediction > 0.5:
                results[image_url] = "Deepfake detected"
            else:
                results[image_url] = "No deepfake detected"
        except Exception as e:
            results[image_url] = f"Error processing image: {str(e)}"
    
    return results

def download_image(image_url):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open("temp_image.jpg", 'wb') as file:
                file.write(response.content)
            return "temp_image.jpg"
        else:
            return None
    except Exception:
        return None
