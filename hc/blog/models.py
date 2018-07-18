from django.db import models
from hc.accounts.models import User
from django.utils import timezone


STATUS_CHOICES = (
	('draft', 'Draft'),
	('published', 'published'))


class Category(models.Model):
	name = models.CharField(max_length=30)


class Blog(models.Model):
	title = models.CharField(max_length=100, unique=True, default='Title')
	body = models.TextField(max_length=2000, null=True)
	tags = models.CharField(max_length=500, blank=True, null=True)
	slug = models.SlugField(max_length=250, unique_for_date='published_on')
	author = models.ForeignKey(User, blank=True, null=True)
	published_on = models.DateField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	categories = models.ManyToManyField(Category)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	class Meta:
		ordering = ('-published_on',)

	def __str__(self):
		return self.title


