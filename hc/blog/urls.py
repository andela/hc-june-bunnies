from django.conf.urls import include, url
from hc.blog import views

urlpatterns = [
    url(r'^blog/', views.blogs_list, name="hc-blog-list"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', views.blog_detail, name='hc-blog-detail'),
]