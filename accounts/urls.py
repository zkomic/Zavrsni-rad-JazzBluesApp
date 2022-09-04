from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'


urlpatterns = [
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.login_fun, name="login"),
    url(r'^logout/$', views.logout_fun, name="logout"),
]