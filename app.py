from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

app = Flask(__name__)

# Load the trained model
model = load_model('lumpy_skin_detection_model.h5')

# Define a function for prediction
def predict_lsd(image_path):
    img = load_img(image_path, target_size=(150, 150))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    return "Lumpy Detected" if prediction[0][0] > 0.5 else "No Lumpy Detected"

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    file_path = "static/uploads/" + file.filename
    file.save(file_path)

    result = predict_lsd(file_path)
    return render_template('result.html', result=result, image=file_path)

if __name__ == '__main__':
    app.run(debug=True)
