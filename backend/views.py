from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Img_predictions, Instrument
from django.core.files.storage import default_storage
from PIL import Image
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import load_model
import os
from django.core.files.base import ContentFile
from django.conf import settings
import uuid

class InstrumentList(APIView):
    def get(self, request, *args, **kwargs):
        # Truy vấn tất cả các nhạc cụ từ cơ sở dữ liệu
        instruments = Instrument.objects.all()
        # Chuẩn bị dữ liệu để trả về dưới dạng JSON
        data = []
        for instrument in instruments:
            data.append({
                'name': instrument.name,
                'description': instrument.description,
            })
        # Trả về JSON response
        return Response(data, status=status.HTTP_200_OK)

# Đường dẫn đến mô hình đã lưu
model_path = "E:/Niên Luận/RICE LEAF DISEASES/CODE/backend/models/lenet_model30.h5"

# Tải mô hình đã huấn luyện
model = load_model(model_path)

# Các nhãn của các loại bệnh
categories = ['Brownspot', 'Blast', 'Bacterialblight', 'Tungro']

class ImageDetectAPI(APIView):

    def post(self, request, *args, **kwargs):
        # Lấy ảnh từ request
        image_input = request.FILES.get('image_input')

        if not image_input:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
        

        # img = Img_predictions.objects.create(image=image_input)
        # img.save()

        try:
            
            # Process the image (prepare_image function)
            image = self.prepare_image(image_input)

            
            # Dự đoán loại bệnh từ ảnh
            prediction = model.predict(image)
            predicted_class = np.argmax(prediction, axis=1)
            label = categories[predicted_class[0]]

            return Response({'output': label})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def prepare_image(self, image_file):
        # Đọc hình ảnh từ file
        image = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        
        # Resize hình ảnh theo đúng kích thước mà mô hình yêu cầu
        image = cv2.resize(image, (64, 64))
        
        # Chuyển đổi hình ảnh thành array và normalize
        image = np.array(image, dtype="float") / 255.0
        
        # Thêm một dimension để phù hợp với đầu vào của mô hình (batch size)
        image = np.expand_dims(image, axis=0)
        
        return image



# Phân loại nhiều nhãn trên 1 hình
# class ImageDetectAPI(APIView):

#     def post(self, request, *args, **kwargs):
#         # Lấy ảnh từ request
#         image_input = request.FILES.get('image_input')

#         if not image_input:
#             return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Xử lý ảnh (sử dụng hàm prepare_image)
#             image = self.prepare_image(image_input)

#             # Dự đoán loại bệnh từ ảnh
#             prediction = model.predict(image)[0]  # Lấy đầu ra đầu tiên (batch size = 1)
            
#             # Tìm các nhãn có xác suất cao hơn ngưỡng (ví dụ: 0.5)
#             threshold = 0.5
#             predicted_labels = [categories[i] for i in range(len(categories)) if prediction[i] >= threshold]

#             if not predicted_labels:
#                 predicted_labels = ["No disease detected"]

#             return Response({'output': predicted_labels})
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def prepare_image(self, image_file):
#         # Đọc hình ảnh từ file
#         image = np.frombuffer(image_file.read(), np.uint8)
#         image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        
#         # Resize hình ảnh theo đúng kích thước mà mô hình yêu cầu
#         image = cv2.resize(image, (64, 64))
        
#         # Chuyển đổi hình ảnh thành array và normalize
#         image = np.array(image, dtype="float") / 255.0
        
#         # Thêm một dimension để phù hợp với đầu vào của mô hình (batch size)
#         image = np.expand_dims(image, axis=0)
        
#         return image