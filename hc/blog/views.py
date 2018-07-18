from django.shortcuts import render, get_object_or_404
from hc.blog.models import Blog
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def blogs_list(request):
	'''displays a list of all published blogs'''
	published_blogs = Blog.published.all()
	ctx = {
		'blogs': published_blogs
	}
	return render(request, "blog/blogs_list.html", ctx)


@login_required
def blog_detail(request, year, month, day, slug):
	blog = get_object_or_404(Blog, slug=slug, status='published', published_on__year=year, published_on__month=month, published_on__day=day)
	ctx = {'blog': blog}
	return render(request, 'blog/blog_detail.html', ctx)