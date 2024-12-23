from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.views import View
from django.urls import reverse
from .models import Video, Comment
from .forms import AddCommentForm, AddVideoForm, CreateChannelForm


def index(request):   
    data = {'videos': Video.objects.all()}
    return render(request, 'mytube/index.html', data)



class Prof(View):
    '''Страница профиля пользователя'''

    @staticmethod
    def get(request, prof_name):
        try:
            author_channel = get_user_model().objects.get(name=prof_name)
        except:
            return HttpResponseNotFound
        
        subscribe_status = author_channel.is_subscribed(request.user)
        
        template = 'mytube/channel.html'
        data = {'title': prof_name,
                'author_channel': author_channel,
                'subscribe_status': subscribe_status,}
        
        return render(request, template, data)
    


class CreateChannel(LoginRequiredMixin, View):
    '''Форма изменения профиля'''

    @staticmethod
    def get(request):
        form = CreateChannelForm
        template = 'form_post.html'
        data = {'title': 'Создание канала',
                'title_btn': 'Сохранить',
                'form': form}
        return render(request, template, data)
    
    @staticmethod
    def post(request):
        form = CreateChannelForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('prof', prof_name=form.cleaned_data['name'])



class UpLoadVideo(LoginRequiredMixin, View):
    "Форма загрузки видео"

    template = 'form_post.html'
    form = AddVideoForm
    data = {'title': 'Загрузка видео',
            'title_btn': 'Загрузить',
            'form': form}


    def get(self, request):
        return render(request, self.template, self.data)
    
    
    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user
            video.save()
            return redirect('prof', prof_name=request.user.name)
    


class AccountManagement(LoginRequiredMixin, View):
    '''Страница управления аккаунтом'''

    def get(self, request):
        data = {'title': 'Управление аккаунтом'}
        return render(request, 'mytube/account_management.html', data)
    


class PlayerVideo(View):
    '''Страница показа видео'''

    @staticmethod
    def get(request, video_name):
        template = 'mytube/video_player.html' 

        try:
            video = Video.objects.get(name = video_name)
        except:
            return HttpResponseNotFound
        
        reaction = video.reaction_checks(request.user)
        subscribe_status = video.author.is_subscribed(request.user)

        data = {
            'video': video,
            'form': AddCommentForm,
            'reaction': reaction,
            'subscribe_status': subscribe_status,
            }
        return render(request, template, data)
    

class CreateComment(LoginRequiredMixin, View):
    '''Добавление комментария'''

    @staticmethod
    def post(request):
        response = HttpResponse()
        try:
            user = request.user
            video_name = request.POST.get('video')
            video = Video.objects.get(name=video_name)
            text = request.POST.get('text')
            com = Comment.objects.create(text=text, author=user, video=video)
            com.save()
            response.status_code = 200
        except:
            response.status_code = 404

        return response


class LikeVideo(LoginRequiredMixin, View):
    '''Возможность ставить лайки и дизлайки'''

    @staticmethod
    def post(request):
        response = HttpResponse()
        user = request.user
        
        #Пытаемся получить обьект видео
        try:
            video_name = request.POST.get('video_name') 
            video = Video.objects.get(name = video_name)
        except:
            print('неверно указанно видео')
            response.status_code = 404
            return response
        
        if video.author == user:
            response.status_code = 404
            
        
        like_dict = {'like': video.liked_by, 
                     'dislike': video.disliked_by}
        
        new_status = request.POST.get("status")

        #проверка какая оценка была до
        old_status = video.reaction_checks(user)

        #Убираем оценку(если новая и старая совпадают)
        if old_status == new_status:
            try:
                like_dict[new_status].remove(user)
                response.status_code = 202
            except:
                response.status_code = 404
        
        #Ставим оценку если до этого её не было
        elif not old_status:
            try:
                like_dict[new_status].add(user)
                response.status_code = 200
            except:
                response.status_code = 404
            
        #Меняем оценку на другую
        else:
            try:
                like_dict[new_status].add(user)
                like_dict[old_status].remove(user)
                response.status_code = 201
            except:
                response.status_code = 404
            
        if response.status_code != 404:
            video.save()

        return response
            
        
class Subscribe(LoginRequiredMixin, View):
    '''Функция подписки на канал'''

    @staticmethod
    def post(request):
        user = request.user
        response = HttpResponse()
        channel_name = request.POST.get('channel_name')
        channel = get_user_model().objects.get(name=channel_name)
        try:
            if channel.is_subscribed(user):
                channel.subscribers.remove(user)
                response.status_code = 201
            else:
                channel.subscribers.add(user)
                response.status_code = 200
        except:
            response.status_code = 404
        return response


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1><a href="">Вернуться на главную</a>')

