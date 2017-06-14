from django.conf.urls import url
from core.views import (
    SearchView,
    AppsView,
    AppView
)

urlpatterns = [
    url(r'^search$', AppsView.as_view(), name='search'),
    url(r'^$', SearchView.as_view(), name='home'),
]
