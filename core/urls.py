from django.conf.urls import url
from core.views import (
    SearchView,
    AppsView,
    AppView
)

urlpatterns = [
    url(r'^search$', AppsView.as_view(), name='search'),
    url(r'^app$', AppView.as_view(), name='app-detail'),
    url(r'^$', SearchView.as_view(), name='home'),
]
