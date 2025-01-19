from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View

from .forms import LoginUserForm, RegisterUserForm



class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Вход в аккаунт'}

class  Register(View):
    """Форма регистрации на сайте"""

    @staticmethod
    def post(request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)   
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/register_done.html')
    

    @staticmethod
    def get(request):
        form = RegisterUserForm
        data = {'title': 'Регистрация',
                'title_btn': 'Зарегистрироваться',
                'form': form}
        return render(request, 'form_post.html', data)


