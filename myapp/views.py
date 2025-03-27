from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RadioShow
from .serializers import RadioShowSerializer
from .utils import upload_to_dropbox
from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return render(request, 'build/index.html')

def handle_upload(request, file_key, show_name, show_date, genre1, genre2, genre3):
    if request.method == 'POST' and file_key in request.FILES:
        file = request.FILES[file_key]
        
        # Upload the file to Dropbox
        dropbox_url = upload_to_dropbox(request, file, show_name, show_date, genre1, genre2, genre3)
        
        if dropbox_url:
            return dropbox_url  # Return the URL directly
        else:
            return None  # Return None if upload fails
    
    return None  # Return None if no file is uploaded


class RadioShowCreateView(APIView):

    def post(self, request):
        # First, serialize the radio show data
        serializer = RadioShowSerializer(data=request.data)
        if serializer.is_valid():
            # Create the show instance (without media URLs yet)
            show = serializer.save()

            # Handle image upload if provided
            if 'show_image_url' in request.FILES:
                image_url = handle_upload(
                    request, 'show_image_url',
                    show.show_name, show.show_date, show.genre1, show.genre2, show.genre3
                )
                if image_url:
                    show.show_image_url = image_url
                else:
                    return JsonResponse({"status": "error", "message": "Failed to upload image to Dropbox"}, status=status.HTTP_400_BAD_REQUEST)

            # Handle pre-recorded audio upload if provided
            if 'pre_record_url' in request.FILES:
                audio_url = handle_upload(
                    request, 'pre_record_url',
                    show.show_name, show.show_date, show.genre1, show.genre2, show.genre3
                )
                if audio_url:
                    show.pre_record_url = audio_url
                else:
                    return JsonResponse({"status": "error", "message": "Failed to upload pre-recorded audio to Dropbox"}, status=status.HTTP_400_BAD_REQUEST)

            # Save the show with updated URLs
            show.save()

            # Return success message
            return Response({"message": "Radio show created successfully!"}, status=status.HTTP_201_CREATED)

        # If serializer is not valid, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
