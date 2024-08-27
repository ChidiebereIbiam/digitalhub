from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Post


# Create your views here.
def blog(request):
    context = {}
    
    try:
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        most_recent = posts[0]
        other_recent = posts[1:3]

        context = {
            'posts': posts,
            'page_obj': page_obj,
            'most_recent': most_recent,
            'other_recent': other_recent
        }
    except IndexError:
        pass
    return render(request, 'blog/blog.html', context)


def blog_details(request, slug):
    post = get_object_or_404(Post, slug=slug)

    recent_articles = Post.objects.filter(draft=False).order_by('-id')[0:3]
    context = {
        'post': post,
        'recent_articles': recent_articles,

    }
    return render(request, 'blog/blog-details.html', context)
