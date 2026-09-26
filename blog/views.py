from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from blog.models import BlogPost


# 1. READ (Список статей) — Выводим только опубликованные
class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).order_by("-created_at")


# 2. READ (Детальная страница) — Увеличение счетчика + отправка email
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()


        if obj.views_count == 100:
            send_mail(
                subject="Поздравляем с достижением!",
                message=f'Ваша блоговая запись "{obj.title}" набрала 100 просмотров!',
                from_email=settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@test.com',
                recipient_list=["alexei.vishnitsky@yandex.ru"],
                fail_silently=True,
            )

        return obj


# 3. CREATE (Создание статьи)
class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ("title", "content", "preview", "is_published")
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:list")


# 4. UPDATE (Редактирование статьи) — Перенаправление на саму статью
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ("title", "content", "preview", "is_published")
    template_name = "blog/blog_form.html"

    def get_success_url(self):
        return reverse("blog:detail", kwargs={"pk": self.object.pk})


# 5. DELETE (Удаление статьи)
class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:list")
