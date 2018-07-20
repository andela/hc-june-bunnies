from django.conf.urls import include, url
from hc.blog import views

urlpatterns = [
    url(r'^blogs/', views.blogs_list, name="hc-blog-list"),
    url(r'^blog/post/$', views.create_blog, name="hc-post-blog"),
    url(r'^blog/category/(?P<id>[0-9]+)/$', views.get_by_category, name="hc-blog-by_cat"),
    url(r'^blog/drafts/$', views.drafts, name="hc-blog-drafts"),
    url(r'^blog/drafts/delete/(?P<id>[0-9]+)/$', views.delete_blog, name="hc-delete-blog"),
    url(r'^blog/drafts/update/(?P<id>[0-9]+)/$', views.update_blog, name="hc-update-blog"),
    url(r'^blog/publish/(?P<id>[0-9]+)/$', views.publish_blog, name="hc-publish-blog"),
    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', views.blog_detail, name='hc-blog-detail'),
]