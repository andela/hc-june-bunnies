import json
from hc.test import BaseTestCase
from hc.blog.models import Blog
from django.urls import reverse


class BlogTestCase(BaseTestCase):
	def create_blog(self):
		url = "/blog/post/"
		form_data = {'title': 'Sample Title', 'body': 'Sample Body', 'tags':'sample, blog', }
		self.client.login(username="alice@example.org", password="password")
		response = self.client.post(url, form_data)

	def test_can_add_blog(self):

		url = "/blog/post/"
		form_data = {'title': 'Sample Title', 'body': 'Sample Body', 'tags':'sample, blog', 'categories': 'Blog' }
		
		self.client.login(username="alice@example.org", password="password")
		response = self.client.post(url, form_data)
                             
		self.assertEqual(200, response.status_code)
		assert Blog.objects.count() == 1
		assert Blog.published.count() == 0

		response = self.client.get('/blog/drafts/')
		self.assertContains(response, "Sample Title", status_code=200)

		form_data = {'title': 'New Title', 'body': 'Sample Body', 'tags':'sample, blog', 'categories': 'Blog' }
		response = self.client.post('/blog/drafts/update/1/', form_data)
		self.assertEqual(response.status_code, 302)


	def test_can_publish_blog(self):
		url = "/blog/post/"
		form_data = {'title': 'Sample Title', 'body': 'Sample Body', 'tags':'sample, blog', 'categories': 'Blog' }
		
		self.client.login(username="alice@example.org", password="password")
		response = self.client.post(url, form_data)
                             
		self.assertEqual(200, response.status_code)
	
		assert Blog.objects.count() == 1

		blog_id = Blog.objects.all().first().id
		response = self.client.post('/blog/publish/{}/'.format(blog_id))
		self.assertEqual(response.status_code, 302)
		self.assertEqual('published', Blog.objects.all().first().status)
		assert Blog.published.count() == 1

	def test_can_view_blog(self):
		self.create_blog()
		draft_blog = Blog.objects.all()[0]
		draft_blog.status = 'published'
		draft_blog.save()
		url = "/blogs/"
		response = self.client.get(url)
		
		self.assertContains(response, "Sample Title", status_code=200)

	def test_create_blog_form_displays(self):
		self.client.login(username="alice@example.org", password="password")
		response = self.client.get('/blog/post/')
		self.assertContains(response, "Enter tags separated by comma ',' ", status_code=200)

	def test_can_get_one_blog(self):
		self.create_blog()
		blog = Blog.objects.all().first()
		blog.status = 'published'
		blog.save()
		url = reverse('hc-blog-detail',
        	args=[blog.published_on.year, blog.published_on.strftime('%m'), blog.published_on.strftime('%d'), blog.slug])
		response = self.client.get(url)
		# self.assertEqual(200, response.status_code)
		self.assertContains(response, 'Sample Title', status_code=200)