from django.core.paginator import Paginator
from django.views.generic.list import ListView


class GetMultipleItensMixin(object):
    def get_columns(self):
        return ()

    def get_itens(self):
        if not self.paginate_by:
            self.paginate_by = 10

        qs = self.get_queryset()
        if qs.count() > 0:
            qs = Paginator(qs, self.paginate_by)

            response = []
            for item in qs.object_list:
                response.append(self.get_item(item))

            return response
        return []

    def get_item(self, item):
        return []


class CustomListView(ListView, GetMultipleItensMixin):
    template_view = 'base/listview.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['columns'] = self.get_columns()
        ctx['itens'] = self.get_itens()
        return ctx