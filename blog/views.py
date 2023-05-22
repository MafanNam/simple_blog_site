from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from .models import Post
from .forms import CommentForm


def het_date(post):
    return post['date']


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'all_posts'


class SinglePostView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            'post': post,
            'tags': post.tags.all(),
            'form': CommentForm(),
            'comments': post.comments.all(),
        }
        return render(request, 'blog/single-post.html', context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse('single_post', args=[slug]))

        context = {
            'post': post,
            'tags': post.tags.all(),
            'form': CommentForm(),
            'comments': post.comments.all(),
        }

        return render(request, 'blog/single-post.html', context)
