from django.conf.urls import url
from howdy import views


urlpatterns = [
    url(r'^$', views.simple_upload),
]