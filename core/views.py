from django.shortcuts import redirect
from django.views.generic import TemplateView
from core.utils import fetch_apps


class SearchView(TemplateView):
    template_name = "core/search.html"


class AppsView(TemplateView):
    template_name = "core/appslist.html"

    def dispatch(self, request, **kwargs):
        query_string = self.request.GET.get('q', '')
        if not query_string:
            return redirect('home')
        return super(AppsView, self).dispatch(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AppsView, self).get_context_data(**kwargs)
        query_string = self.request.GET.get('q')
        context['apps'] = fetch_apps(query_string)
        return context


class AppView(TemplateView):
    template_name = "core/appdetail.html"
