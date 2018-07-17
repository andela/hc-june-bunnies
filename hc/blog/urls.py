from django.conf.urls import include, url
from hc.blog import views

urlpatterns = [
    url(r'^blog/', views.blog, name="hc-blog")
]