from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm



def home(request):
    all_posts = Post.objects.all()
    return render(request, 'social_network/home.html', {'all_posts': all_posts})
def about(request):
    return render(request, 'social_network/about.html', {'title': 'About'})

@login_required
def post_list(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'social_network/post_list.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')  
    else:
        form = PostForm()
    return render(request, 'social_network/create_post.html', {'form': form})

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'social_network/post_form.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'social_network/post_confirm_delete.html', {'post': post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'social_network/post_detail.html', {'post': post})

