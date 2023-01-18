from django.urls import path, include
from face_shape import views
from django.conf.urls.static import static

urlpatterns = [
    path('face_detect/', views.FaceDetectView.as_view(), name='facedetect'),
]