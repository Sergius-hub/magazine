from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Record
from .forms import RecordForm
# Create your views here.


class RecordListView(ListView):
    model = Record

class RecordDetailView(DetailView):
    model = Record

class RecordCreateView(CreateView):
    model = Record
    form_class = RecordForm
    success_url = reverse_lazy( "blog:record_list" )

    def form_valid( self, form ):
        title = form.cleaned_data["title"]

        # Здесь можно отправить письмо, сохранить в файл,
        # отправить данные в Telegram, CRM и т.д.
        print( title )

        messages.success(
            self.request,
            f"{title} успешно добавлен"
        )

        return super().form_valid( form )