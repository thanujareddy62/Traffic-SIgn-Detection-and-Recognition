from flask import Flask, request, render_template
from flask_cors import CORS
from keras.models import load_model
from PIL import Image
import numpy as np
import os

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Load the trained model
model_path = '/home/student/Desktop/Traffic_Signs_WebApp-master/Traffic_Signs_WebApp-master/training/TSR.h5'
model = load_model(model_path)

# Classes of traffic signs
classes = {
    0: 'Speed limit (20km/h)', 1: 'Speed limit (30km/h)', 2: 'Speed limit (50km/h)', 3: 'Speed limit (60km/h)',
    4: 'Speed limit (70km/h)', 5: 'Speed limit (80km/h)', 6: 'End of speed limit (80km/h)', 7: 'Speed limit (100km/h)',
    8: 'Speed limit (120km/h)', 9: 'No passing', 10: 'No passing vehicles over 3.5 tons',
    11: 'Right-of-way at intersection', 12: 'Priority road', 13: 'Yield', 14: 'Stop', 15: 'No vehicles',
    16: 'Vehicles > 3.5 tons prohibited', 17: 'No entry', 18: 'General caution', 19: 'Dangerous curve left',
    20: 'Dangerous curve right', 21: 'Double curve', 22: 'Bumpy road', 23: 'Slippery road',
    24: 'Road narrows on the right', 25: 'Road work', 26: 'Traffic signals', 27: 'Pedestrians', 28: 'Children crossing',
    29: 'Bicycles crossing', 30: 'Beware of ice/snow', 31: 'Wild animals crossing', 32: 'End of speed and passing limits',
    33: 'Turn right ahead', 34: 'Turn left ahead', 35: 'Ahead only', 36: 'Go straight or right', 37: 'Go straight or left',
    38: 'Keep right', 39: 'Keep left', 40: 'Roundabout mandatory', 41: 'End of no passing',
    42: 'End of no passing vehicles > 3.5 tons'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    if not file:
        return render_template('index.html', error='No file uploaded')

    # Save the uploaded image temporarily
    upload_folder = 'static/uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    # Process the image for prediction
    image = Image.open(filepath).convert('RGB')
    image = image.resize((30, 30))
    image_array = np.array(image).reshape(1, 30, 30, 3)

    # Predict the class
    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction, axis=1)[0]
    predicted_label = classes[predicted_class]

    return render_template('index.html', prediction=predicted_label, image_url=filepath)

if __name__ == '__main__':
    app.run(debug=True)

