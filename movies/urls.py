from django.urls import path
from . import views
# urls.py
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.movie_list,name='movie_list'),
    path('<str:name>/theaters',views.theater_list,name='theater_list'),
    path('theater/<str:theater_id>/<str:time>/seats/book/',views.book_seats,name='book_seats'),
    path('payment_method/<str:theater_id>/<str:time>/<str:seat_no>', views.payment_method, name='payment_method'),
    path('cancel/<str:theater_id>/<str:time>/<str:seat_no>', views.payment_method, name='cancel'),
   path('all-theaters/', views.unique_theater_movies, name='all_theaters'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)