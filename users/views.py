from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm

User = get_user_model()


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()

        send_mail(
            subject='Добро пожаловать в наш интернет-магазин!',
            message=f'Здравствуйте!\n\nСпасибо за регистрацию на нашем сервисе. Ваш логин для входа: {user.email}',
            from_email=settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'webmaster@localhost',
            recipient_list=[user.email],
            fail_silently=True,
        )

        return super().form_valid(form)


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'



class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
