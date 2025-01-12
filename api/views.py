from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from django.conf import settings

# Load the model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'predictor/models/model.h5')
model = load_model(MODEL_PATH)
CLASS_NAMES = ['Disease A', 'Disease B', 'Disease C', 'Disease D']

class PredictDiseaseView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if 'image' not in request.data:
            return Response({'error': 'No image provided.'}, status=400)
        
        try:
            # Get the uploaded image
            uploaded_file = request.data['image']
            temp_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(temp_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Preprocess the image
            image = cv2.imread(temp_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image_size = (224, 224)  # Replace with your model's input size
            resized_image = cv2.resize(gray_image, image_size)
            equalized_image = cv2.equalizeHist(resized_image)
            denoised_image = cv2.medianBlur(equalized_image, ksize=3)
            kernel = np.ones((3, 3), np.uint8)
            eroded_image = cv2.erode(denoised_image, kernel, iterations=1)
            morph_image = cv2.dilate(eroded_image, kernel, iterations=1)
            pixel_values = morph_image.reshape((-1, 1))
            pixel_values = np.float32(pixel_values)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, labels, centers = cv2.kmeans(pixel_values, 2, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            segmented_image = centers[labels.flatten()].reshape(morph_image.shape)

            # Normalize and prepare input
            segmented_image = segmented_image / 255.0
            segmented_image = np.expand_dims(segmented_image, axis=-1)
            segmented_image = np.expand_dims(segmented_image, axis=0)

            # Predict
            predictions = model.predict(segmented_image)
            predicted_class = CLASS_NAMES[np.argmax(predictions)]
            confidence = np.max(predictions)

            os.remove(temp_path)

            return Response({'class': predicted_class, 'confidence': float(confidence)})

        except Exception as e:
            return Response({'error': str(e)}, status=500)
