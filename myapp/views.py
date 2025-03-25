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

def handle_upload(request):
    if request.method == 'POST' and 'show_image_url' in request.FILES:
        show_image = request.FILES['show_image_url']
        
        # Upload the file to Dropbox
        dropbox_url = upload_to_dropbox(request, show_image)
        
        if dropbox_url:
            return dropbox_url  # Just return the URL directly
        else:
            return None  # Return None if upload fails
    
    return None  # Return None if no file is uploaded

class RadioShowCreateView(APIView):

  def post(self, request):
        # First, serialize the radio show data
        serializer = RadioShowSerializer(data=request.data)
        if serializer.is_valid():
            # Create the show instance (without the image URL yet)
            show = serializer.save()

            # Check if there is an image file being uploaded
            if 'show_image_url' in request.FILES:
                image_file = request.FILES['show_image_url']
                # Upload the image to Dropbox (or any other service you're using)
                dropbox_url = upload_to_dropbox(request, image_file)
                
                if dropbox_url:
                    # Update the show instance with the uploaded image URL
                    show.show_image_url = dropbox_url
                    show.save()  # Save the show with the image URL

                else:
                    # If upload fails, return an error
                    return JsonResponse({"status": "error", "message": "Failed to upload image to Dropbox"}, status=status.HTTP_400_BAD_REQUEST)

            # If all goes well, return success message
            return Response({"message": "Radio show created successfully!"}, status=status.HTTP_201_CREATED)

        # If serializer is not valid, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)