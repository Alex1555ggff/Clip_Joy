from django.conf.urls.static import static
from django.urls import path
from . import views
from myvlog import settings


urlpatterns = [
    path('', views.index, name='main'),

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

    path('comment', views.CreateComment.as_view(), name="comment"),
    path('like', views.LikeVideo.as_view(), name="like"),
    path('subscribe', views.Subscribe.as_view(), name='subscribe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found

