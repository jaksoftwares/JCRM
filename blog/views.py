from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Category, Comment
from .forms import CommentForm

def blog_list(request):
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blog/blog_list.html', {'posts': posts, 'categories': categories})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    comments = post.comments.filter(approved=True)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog_detail', slug=post.slug)

    return render(request, 'blog/blog_detail.html', {'post': post, 'comments': comments, 'form': form})

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(published=True)
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})
