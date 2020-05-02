from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages

from django.views.generic import TemplateView, ListView, DetailView,\
    CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment, About

# Create your views here.


class AboutDetailView(ListView):
    model = About

    def get_queryset(self):
        return About.objects.all()


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


@login_required
def create_post(request):
    author = request.user
    if request.method=='POST':
        title = request.POST['title']
        text = request.POST['text']

        post = Post(author=author, title=title, text=text)
        post.save()
        return redirect('post_draft_list')

    return render(request, 'blog/post_form.html')


# class CreatePostView(LoginRequiredMixin, CreateView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_detail.html'
#     form_class = PostForm
#     model = Post


@login_required
def post_update_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        title = request.POST['title']
        text = request.POST['text']
        post.title=title
        post.text=text
        post.save()
        messages.success(request, message="Successfully updated!")
        return redirect('post_detail', pk=pk)

    return render(request, 'blog/post_edit.html', context={'post':post})


# class PostUpdateView(LoginRequiredMixin, UpdateView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_detail.html'
#     form_class = PostForm
#     model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


def draft_list_view(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('create_date')

    return render(request, 'blog/draft_list.html', context={'posts': posts})

@login_required
def draft_detail_view(request, pk):
    post = Post.objects.filter(pk=pk)[0]
    return render(request, 'blog/draft_detail.html', context={'post':post})

# class DraftListView(LoginRequiredMixin, ListView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_draft_list.html'
#     model = Post
#
#     def get_queryset(self):
#         return Post.objects.filter(published_date__isnull=True).order_by('create_date')

###############################################################
###############################################################


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        author = request.POST['author']
        text = request.POST['text']
        comment = Comment(post=post, author=author, text=text)
        comment.save()
        messages.success(request, message="Your comment will pop up upon author's approval")
        return redirect('post_detail', pk=pk)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    messages.success(request, message="Comment approved!")
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, message="Comment removed!")
    return redirect('post_detail', pk=post_pk)
