from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('populate/', views.populate_database, name='populate'),
    path('clear-data/', views.clear_data, name='clear_data'),
    path('clear-cache/', views.clear_cache, name='clear_cache'),
    path('update_interval/', views.update_interval, name='update_interval'),
    path('new_interval/', views.new_interval, name='new_interval'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
