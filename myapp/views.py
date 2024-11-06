from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RadioShow
from .serializers import RadioShowSerializer
from .utils import upload_to_dropbox
from django.shortcuts import render


def index(request):
    return render(request, 'build/index.html')

class RadioShowCreateView(APIView):
    
    def post(self, request):
        data = request.data
        form = RadioShowSerializer(data=data)

        if form.is_valid():
            show = form.save(commit=False)

            # Check if there's an image file being uploaded
            if 'show_image_url' in request.FILES:
                file = request.FILES['show_image_url']
                
                # Upload the file to Dropbox
                show_image_url = upload_to_dropbox(file)
                show.show_image_url = show_image_url
            
            # Save the show record in the database
            show.save()

            # Return success response
            return Response({"message": "Radio show created successfully!"}, status=status.HTTP_201_CREATED)
        
        # If form is not valid, return the validation errors
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
