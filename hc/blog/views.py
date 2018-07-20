from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from hc.blog.forms import BlogForm
from hc.blog.models import Blog, Category, Tag
from django.template.defaultfilters import slugify
from django.http import Http404



def blogs_list(request):
	'''displays a list of all published blogs'''
	published_blogs = Blog.published.all()
	categories = Category.objects.all().order_by('name')
	ctx = {
		'blogs': published_blogs,
		'categories': categories
	}
	return render(request, "blog/blogs_list.html", ctx)



def blog_detail(request, year, month, day, slug):
	blog = Blog.objects.filter(slug=slug, published_on__year=year, published_on__month=month, published_on__day=day).first()
	if not blog:
		raise Http404

	ctx = {'blog': blog}
	return render(request, 'blog/blog_detail.html', ctx)


@login_required
def create_blog(request):
	if request.method == "POST":
		form = BlogForm(request.POST)
		if form.is_valid():
			# get blog data
			title = form.cleaned_data['title']
			body = form.cleaned_data['body']
			tags = form.cleaned_data['tags']
			categories = form.cleaned_data['categories']
			slug = slugify(title)
			blog = Blog(title=title, body=body, author=request.user, slug=slug)
			blog.save()
			categories = categories.split(',')
			tags = tags.split(',')
			for category in categories:
				cat = Category.objects.filter(name=category).first()
				if not cat:
					cat = Category(name=category)
					cat.save()
				blog.categories.add(cat.id)

			for tag in tags:
				tag_ = Tag.objects.filter(name=tag).first()
				if not tag_:
					tag_ = Tag.objects.create(name=tag)

				blog.tags.add(tag_.id)
			blog.save()

			
			ctx = {'blog': blog}
			return render(request, 'blog/blog_detail.html', ctx)
	
	form = BlogForm()
	ctx = {'form': form}
	return render(request, 'blog/post_blog.html', ctx)

@login_required
def drafts(request):
	draft_blogs = Blog.objects.filter(author=request.user, status='draft').all()
	ctx = {'blogs': list(draft_blogs)}
	return render(request, 'blog/blogs_list.html', ctx)
			
@login_required
def publish_blog(request, id):
	assert request.method == 'POST'
	blog = Blog.objects.filter(id=id).first()
	if not blog:
		raise Http404
	blog.status = 'published'
	blog.save()
	return redirect('hc-blog-list')

@login_required
def update_blog(request, id):
	assert request.method == 'POST'
	blog = Blog.objects.filter(id=id).first()
	if not blog:
		raise Http404
	form = form = BlogForm(request.POST)
	if form.is_valid():
		# get blog data
		title = form.cleaned_data['title']
		body = form.cleaned_data['body']
		tags = form.cleaned_data['tags']
		categories = form.cleaned_data['categories']
		slug = slugify(title)
		categories = categories.split(',')
		tags = tags.split(',')
		for category in categories:
			cat = Category.objects.filter(name=category).first()
			if not cat:
				cat = Category(name=category)
				cat.save()
			blog.categories.add(cat.id)

		for tag in tags:
			tag_ = Tag.objects.filter(name=tag).first()
			if not tag_:
				tag_ = Tag.objects.create(name=tag)

			blog.tags.add(tag_.id)
		blog.save()
	
	return redirect('hc-blog-list')

@login_required
def delete_blog(request, id):
	blog = Blog.objects.filter(id=id).first()
	if not blog:
		raise Http404
	blog.delete()

	return redirect('hc-blog-list')

def get_by_category(request, id):
	category = Category.objects.filter(id=id).first()
	cat_blogs = category.blog_set.all()
	categories = Category.objects.all().order_by('name')
	ctx = {
		'title': category.name,
		'blogs': cat_blogs,
		'categories': categories
	}
	return render(request, "blog/blogs_list.html", ctx)
