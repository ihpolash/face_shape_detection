from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, serializers, status
from rest_framework.generics import GenericAPIView

# Create your views here.
from rest_framework.response import Response
import client
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class FaceShapeDetectSerializer(serializers.Serializer):
    image = serializers.ImageField()

class FaceShapeDetectView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FaceShapeDetectSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data.get('image')
        response = client.face_detect(image)
        return Response(response, status=status.HTTP_200_OK)
