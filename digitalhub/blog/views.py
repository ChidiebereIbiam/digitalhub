from django.shortcuts import render

# Create your views here.

def blog(request):
    context = {}
    return render(request, 'blog/blog.html', context)


def blog_details(request, slug):
    context = {}
    return render(request, 'blog/blog-details.html', context)