from django.urls import path, include
from rest_framework import routers
from .views import PizzariaListView, PizzariaDetailView, PizzariaCreateView, PizzariaViewSet, pizzeria_list, \
    PizzerriaApiView, PizzeriaNewApi, SnippetListView, SnippetDetailView, UserListView, UserDetailView, AlbumView, TrackView

router = routers.SimpleRouter()
router.register(r'set', PizzariaViewSet)
urlpatterns = [
    # path('', include(router.urls)),
    path('list/', PizzariaListView.as_view(), name='list'),
    path('detail/<int:pk>', PizzariaDetailView.as_view(), name='detail'),
    path('create/', PizzariaCreateView.as_view(), name='create'),
    path('func/', pizzeria_list),
    path('func/<int:pk>/', pizzeria_list),
    path('class/<int:pk>/', PizzerriaApiView.as_view()),
    path('generic/<int:pk>/', PizzeriaNewApi.as_view()),
    path('snippet/', SnippetListView.as_view(), name='snippet-list'),
    path('snippet/<int:pk>/', SnippetDetailView.as_view(), name='snippet-detail'),
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('album/', AlbumView.as_view()),
    path('album/<int:pk>/', TrackView.as_view(), name='track-detail'),
]

urlpatterns += [path('', include('rest_framework.urls')), ]
