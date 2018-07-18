from django.contrib import admin
from hc.blog.models import Blog, Category

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ("id", "status", "title", "body", "slug", "author", "published_on",
		"updated")
	list_filter = ('status','published_on','author')
	search_fields = ('title','author')
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('author',)
	date_hierarchy = 'published_on'
	ordering = ['status', 'published_on']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ["id", "name"]
