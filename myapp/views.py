from django.shortcuts import render, redirect
from .forms import RadioShowForm
from .utils import upload_to_dropbox

def submit_show(request):
    if request.method == 'POST':
        form = RadioShowForm(request.POST, request.FILES)
        if form.is_valid():
            show = form.save(commit=False)
            if 'show_image_url' in request.FILES:
                file = request.FILES['show_image_url']
                show_image_url = upload_to_dropbox(file)
                show.show_image_url = show_image_url
            show.save()
            return redirect('success')
    else:
        form = RadioShowForm()
    return render(request, 'submit_show.html', {'form': form})
