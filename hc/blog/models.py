from django.db import models
from hc.accounts.models import User
from django.utils import timezone
from django.urls import reverse


STATUS_CHOICES = (
	('draft', 'Draft'),
	('published', 'published'))


class Category(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name



class PublishedManager(models.Manager):
	'''custom manager to get published blogs'''
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter(status='published')


class Blog(models.Model):
	title = models.CharField(max_length=100, default='Title')
	body = models.TextField(max_length=2000, null=True)
	tags = models.ManyToManyField(Tag)
	slug = models.SlugField(max_length=250, unique_for_date='published_on')
	author = models.ForeignKey(User, blank=True, null=True)
	published_on = models.DateField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	categories = models.ManyToManyField(Category)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	
	published = PublishedManager()
	objects = models.Manager()

	class Meta:
		ordering = ('-published_on',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		'''get an absolute url pointing to a blog post'''
		return reverse(
        	'hc-blog-detail',
        	args=[self.published_on.year, self.published_on.strftime('%m'), self.published_on.strftime('%d'), self.slug])

