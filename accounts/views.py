from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import (TemplateView, CreateView, DetailView, UpdateView, DeleteView,
                                  PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, resolve_url
from .forms import (LoginForm, SignupForm, EditForm, UserPasswordChangeForm,
                    AccountPasswordResetForm, AccountSetPasswordForm)


User = get_user_model()


class AccountLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'


class AccountCreateView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')


class AccountIndexView(TemplateView):
    template_name = 'accounts/index.html'


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = False

    def test_func(self):
        user = self.request.user
        return user.username == self.kwargs['username'] or user.is_superuser


class AccountDetail(OnlyYouMixin, DetailView):
    model = User
    template_name = 'accounts/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class AccountEdit(OnlyYouMixin, UpdateView):
    model = User
    form_class = EditForm
    template_name = 'accounts/edit.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return resolve_url('detail', username=self.kwargs['username'])


class AccountPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'accounts/passwordchange.html'
    success_url = reverse_lazy('passwordchangedone')


class AccountPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/passwordchangedone.html'


class AccountDeleteView(OnlyYouMixin, DeleteView):
    template_name = 'accounts/delete.html'
    success_url = reverse_lazy('login')
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class AccountPasswordResetView(PasswordResetView):
    template_name = 'accounts/passwordreset.html'
    success_url = reverse_lazy('passwordresetdone')
    form_class = AccountPasswordResetForm
    subject_template_name = 'account/mail_template/passwordreset/subject.txt'
    email_template_name = 'account/mail_template/passwordreset/message.txt'


class AccountPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/passwordresetdone.html'


class AccountPasswordConfirmView(PasswordResetConfirmView):
    form_class = AccountSetPasswordForm
    template_name = 'accounts/passwordresetconfirm.html'
    success_url = reverse_lazy('passwordrestcomplete')


class AccountPassrowdResetCompleteView(PasswordResetCompleteView):
    templete_name = 'accounts/passwordresetcomplete.html'
