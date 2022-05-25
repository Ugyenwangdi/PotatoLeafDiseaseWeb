from django.urls import path
from . import views
from django.conf.urls.static import static 
from django.conf import settings

from .views import PotatoAPIView

app_name = 'classifierApp'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('history', views.history, name='historypage'),


    path('predict', views.predictImage),
    path('viewdb', views.viewDataBase, name='view'),

    # path('register', views.register, name='register'),
    
    # path('login/', views.loginUser, name="login"),
    # path('changepw/', views.changePW, name="changepw"),
    # path('logout/', views.logoutUser, name="logout"),  

    path('indexm', views.indexm, name='indexmpage'),

    path('api/routes', views.getRoutes),
    path('api/results/all', PotatoAPIView.as_view()),
    path('api/predict', PotatoAPIView.as_view(), name='predict'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)