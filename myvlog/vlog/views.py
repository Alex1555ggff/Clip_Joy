from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse, FileResponse
from django.template.loader import render_to_string
from django.core.cache import cache
from django.views import View
from django.urls import reverse

from .models import Video, Comment
from .forms import AddCommentForm, AddVideoForm, CreateChannelForm

from pathlib import Path
from typing import IO, Generator

import re


class MainPage(View):
    '''Главная страница'''

    @staticmethod
    def get(request):
        try:
            videos = Video.objects.all().select_related('author')
        except:
            return HttpResponseNotFound

        data = {
            'videos': videos,
            }
        
        return render(request, 'mytube/index.html', data)


class Prof(View):
    '''Страница профиля пользователя'''

    @staticmethod
    def get(request, prof_name):
        author_channel = get_object_or_404(get_user_model(), name=prof_name)
        
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

        video = get_object_or_404(Video, name=video_name)
        
        reaction = video.reaction_checks(request.user)
        subscribe_status = video.author.is_subscribed(request.user)
        comments = video.comment_set.all().select_related('author')

        data = {
            'video': video,
            'form': AddCommentForm,
            'reaction': reaction,
            'subscribe_status': subscribe_status,
            'comments': comments,
            }
        return render(request, template, data)
    

class CreateComment(View):
    '''Добавление комментария'''

    @staticmethod
    def post(request):
        response = HttpResponse()
        try:
            user = request.user
            if not user.is_authenticated:
                response.status_code = 401
                return response
        
            video_name = request.POST.get('video')
            video = Video.objects.get(name=video_name)
            text = request.POST.get('text')
            com = Comment.objects.create(text=text, author=user, video=video)
            com.save()
            response.status_code = 200
        except:
            response.status_code = 404

        return response


class LikeVideo(View):
    '''Возможность ставить лайки и дизлайки'''

    @staticmethod
    def post(request):
        response = HttpResponse()
        user = request.user
        
        if not user.is_authenticated:
            response.status_code = 401
            return response

        #Пытаемся получить обьект видео
        video_name = request.POST.get('video_name') 
        video = get_object_or_404(Video, name=video_name)
        
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
            
        
class Subscribe(View):
    '''Функция подписки на канал'''

    @staticmethod
    def post(request):
        user = request.user
        response = HttpResponse()

        if not user.is_authenticated:
            response.status_code = 401
            return response
        
        channel_name = request.POST.get('channel_name')
        channel = get_object_or_404(get_user_model(), name=channel_name)
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


class DeleteVideo(View):
    '''Удаление видео'''

    @staticmethod
    def post(request):
        video_name = request.POST.get('video_name')
        video = get_object_or_404(Video, name=video_name)
        response = HttpResponse()

        if video.author.username == request.user.username:
            video.delete()
            response.status_code = 200
            return response
        else:
            response.status_code = 404
            return response
        

'''def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


def open_file(request, video_id: int) -> tuple:
    _video = get_object_or_404(Video, pk=video_id)

    path = Path(_video.video.path)

    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    content_range = request.headers.get('range')

    if content_range is not None:
        content_ranges = content_range.strip().lower().split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        content_range = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, content_range'''


def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end is not None else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += len(data)
        yield data

    if hasattr(file, 'close'):
        file.close()


def get_streaming_video(request, pk: int):
    _video = get_object_or_404(Video, pk=pk)
    file_path = Path(_video.video.path)
    file_size = file_path.stat().st_size
    content_type = 'video/mp4'  # Предполагаем, что видео в формате MP4, измените при необходимости

    range_header = request.headers.get('range')

    if range_header:
        match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        if not match:
            return HttpResponse("Invalid Range header", status=400)

        start_str, end_str = match.groups()
        start = int(start_str)
        end = int(end_str) if end_str else file_size - 1
        start = max(0, start)
        end = min(file_size - 1, end)

        if start > end:
            return HttpResponse("Range Not Satisfiable", status=416)

        content_length = end - start + 1
        response = StreamingHttpResponse(
            ranged(file_path.open('rb'), start=start, end=end + 1),
            status=206,
            content_type=content_type,
        )
        response['Content-Length'] = str(content_length)
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
    else:
        response = FileResponse(file_path.open('rb'), content_type=content_type)
        response['Content-Length'] = str(file_size)

    response['Accept-Ranges'] = 'bytes'
    return response

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1><a href="">Вернуться на главную</a>')

