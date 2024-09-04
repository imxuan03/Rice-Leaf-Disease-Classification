from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import ImageDetectAPI,InstrumentList, RasaChatbotAPIView

urlpatterns = [
    path('api/instrument/', InstrumentList.as_view(), name='instrument_list'),
    path('api/detect/', ImageDetectAPI.as_view(), name='image-detect-api'),
    path('api/chat/', RasaChatbotAPIView.as_view(), name='rasa_chatbot_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)