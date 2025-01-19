from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.urls import path
from . import views
from myvlog import settings


urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),

    path('account_management/',
         views.AccountManagement.as_view(),
         name='account_management'),

    path('account_management/upload_video/',
         views.UpLoadVideo.as_view(),
         name='upload_video'),

    path('account_management/create_channel/',
         views.CreateChannel.as_view(),
         name="create_channel"),

    path('profile/<str:prof_name>', views.Prof.as_view(), name="prof"),
    path('watch/<str:video_name>', views.PlayerVideo.as_view(), name="watch"),
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),

    path('comment', views.CreateComment.as_view(), name="comment"),
    path('like', views.LikeVideo.as_view(), name="like"),
    path('subscribe', views.Subscribe.as_view(), name='subscribe'),
    path('delete_video', views.DeleteVideo.as_view(), name='delete_video'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found

