from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import uploadform, PostForm, SignUpForm, EditProfileForm, PasswordChangingForm, CommentForm
from .models import History, Post,Category,Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import pytesseract    # ======= > Add
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User



# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def error(request):
    return render(request, 'error.html')

class HistoryListView(ListView):
    def get_queryset(self):
        return History.objects.filter(user=self.request.user).order_by('-date')
    template_name = 'history.html'
    context_object_name = 'Histories'
    paginate_by = 10


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

class UserRegisterView(CreateView):
    form_class = SignUpForm
    template_name = "register.html"
    success_url = reverse_lazy('login')

class PostListView(ListView):
    model = Post
    template_name = "blog.html"
    context_object_name = "Posts"
    ordering = ['-date']
    paginate_by = 10
    def get_context_data(self, *arg, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostListView, self).get_context_data(*arg, **kwargs)
        context['cat_menu'] = cat_menu
        return context

class PostDetailView(DetailView):
    model = Post
    form_class = CommentForm
    template_name = "post.html"
    context_object_name = 'post'
    def post(self, request, *args, **kwargs):
        form = CommentForm(body = request.POST.get('body'), author = request.user, post=self.get_object())
        form.save()
        self.get(self, request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('post', kwargs={'pk': self.kwargs['pk']}))

    def get_context_data(self, *arg, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetailView, self).get_context_data(*arg, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        liked = stuff.likes.filter(id = self.request.user.id).exists()
        comments_connected = Comment.objects.filter(post=self.get_object()).order_by('-date')
        context['comments'] = comments_connected
        context['cat_menu'] = cat_menu
        context['total_likes'] = total_likes
        context['liked'] = liked
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm(instance=self.request.user)
        return context

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.kwargs['pk']})

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "add_post.html"
    

class UpdatePostView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "update_post.html"

class DeletePostView(DeleteView):
    model = Post
    template_name = "delete_post.html"
    context_object_name = 'post'
    success_url = reverse_lazy('blog')


class UserEditView(UpdateView):
    form_class = EditProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

def CategoryView(request, cats):
    cat_menu = Category.objects.all()
    category_posts = Post.objects.filter(category = cats)
    return render(request, 'category.html', {'cats':cats, 'category_posts': category_posts, 'cat_menu': cat_menu})

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post', args=[str(pk)]))

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'password_success.html')

class ShowProfilePageView(DetailView):
    model = User
    template_name = 'user_profile.html'

    def get_context_data(self, *arg, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*arg, **kwargs)
        page_user = get_object_or_404(User, id=self.kwargs['pk'])
        context['page_user'] = page_user

        return context