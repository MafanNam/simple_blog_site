from django.shortcuts import render, get_object_or_404

from .models import Post


def het_date(post):
    return post['date']


def index(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]

    context = {
        'posts': latest_posts,
    }
    return render(request, 'blog/index.html', context)


def posts(request):
    all_posts = Post.objects.all().order_by('-date')

    context = {
        'all_posts': all_posts,
    }
    return render(request, 'blog/all-posts.html', context)


def single_post(request, slug):
    one_post = get_object_or_404(Post, slug=slug)

    context = {
        'post': one_post,
        'tags': one_post.tags.all(),
    }
    return render(request, 'blog/single-post.html', context)
