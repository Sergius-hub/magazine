from django.urls import path

from .views import RecordListView, RecordDetailView, RecordCreateView
from .apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path("", RecordListView.as_view(), name="record_list"),
    path("records/<int:pk>", RecordDetailView.as_view(), name="record_detail"),
    path("records/create/", RecordCreateView.as_view(), name="record_create"),

]