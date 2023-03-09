from django.urls import path
from .views import getFiles,uploadFile,createFolder,deleteFile,register_request,profile,download_file
urlpatterns=[
    path('', getFiles,name='home'),
    path('upload/<str:remaining_size>',uploadFile,name='upload'),
    path('delete/<str:id>',deleteFile,name='delete'),
    path("auth/register", register_request,name='register'),
    path('profile',profile,name='profile'),
    path('createFolder',createFolder,name='createfolder'),
    path('download/<str:id>', download_file, name='download_file'),
]