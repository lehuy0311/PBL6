from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import RegistrationForm
from django.views.generic import FormView
from .forms import *
from .models import History
from django.views.generic import ListView
import pytesseract    # ======= > Add
from PIL import Image
from base64 import b64encode
from django.core.files.storage import FileSystemStorage

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# def index(request):
#     return render(request, 'home.html')


def error(request):
    return render(request, 'error.html')


def history(request, pk):
    if request.user.is_authenticated:
        HttpResponseRedirect('login')
    return render(request, 'history.html')


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'register.html', {'form': form})


class HistoryListView(ListView):
    def get_queryset(self):
        return History.objects.filter(user=self.request.user).order_by('-date')
    template_name = 'history.html'
    context_object_name = 'Histories'
    paginate_by = 1


def home(request):
    if request.method == 'POST':
        form = uploadform(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            fss = FileSystemStorage()
            file = fss.save(image.name, image)
            file_url = fss.url(file)
            
            text = pytesseract.image_to_string(
                Image.open(image), lang='jpn')
            if text and request.user.is_authenticated:
                History.objects.create(user=request.user, body=text)

            form = uploadform()
            context = {'form': form, 'image': file_url, 'text': text}
            return render(request, 'home.html', context)
    else:
        form = uploadform()
    return render(request, 'home.html', {'form': form})
