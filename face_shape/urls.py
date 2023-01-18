from django.urls import path, include
from face_shape import views
from django.conf.urls.static import static

urlpatterns = [
    path('face_detect/', views.FaceShapeDetectView.as_view(), name='faceshapedetect'),
]