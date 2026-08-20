from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from .models import Record
from .forms import RecordForm

# Create your views here.


class RecordListView(ListView):
    model = Record

    def get_queryset(self):
        return Record.objects.filter(is_active=True)


class RecordDetailView(DetailView):
    model = Record

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class RecordCreateView(CreateView):
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy("blog:record_list")

    def form_valid(self, form):
        title = form.cleaned_data["title"]

        # Здесь можно отправить письмо, сохранить в файл,
        # отправить данные в Telegram, CRM и т.д.
        print(title)

        messages.success(self.request, f"{title} успешно добавлен")

        return super().form_valid(form)


class RecordUpdateView(UpdateView):
    model = Record
    form_class = RecordForm

    # success_url = reverse_lazy( "blog:record_list" )
    def form_valid(self, form):
        title = form.cleaned_data["title"]

        # Здесь можно отправить письмо, сохранить в файл,
        # отправить данные в Telegram, CRM и т.д.
        print(title)

        messages.success(self.request, f"{title} успешно обновлен")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:record_detail", args=[self.object.pk])


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy("blog:record_confirm_delete")
