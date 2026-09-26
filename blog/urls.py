from django.urls import path
from blog.views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)

app_name = "blog"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="list"),
    path("create/", BlogPostCreateView.as_view(), name="create"),
    path("<int:pk>/", BlogPostDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", BlogPostUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", BlogPostDeleteView.as_view(), name="delete"),
]
