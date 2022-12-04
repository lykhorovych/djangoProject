from django.http import HttpRequest, Http404
from django.shortcuts import render, get_object_or_404
from .models import Pizzeria, Snippet, User, Album, Track
from .serializers import PizzariaListSerializer, PizzariaDetailSerializer, SnippetSerializer, UserSerializer, \
    AlbumSerializer, TrackSerializer
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsOwnerReadOnlyPermission


# Create your views here.
class PizzariaListView(generics.ListAPIView):
    queryset = Pizzeria.objects.all()
    serializer_class = PizzariaListSerializer


class PizzariaDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Pizzeria.objects.all()
    serializer_class = PizzariaDetailSerializer


class PizzariaCreateView(generics.CreateAPIView):
    queryset = Pizzeria.objects.all()
    serializer_class = PizzariaDetailSerializer


class PizzariaViewSet(ViewSet):
    queryset = Pizzeria.objects.all()

    def list(self, request):
        serializer = PizzariaListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = get_object_or_404(self.queryset, pk=pk)
        serializer = PizzariaDetailSerializer(obj)
        return Response(serializer.data)

    def update(self, request, pk=None):
        print(request.method)
        obj = get_object_or_404(self.queryset, pk=pk)
        serializer = PizzariaDetailSerializer(obj)
        if request.method == 'PUT':
            print(request.data)
            serializer = PizzariaDetailSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        obj = get_object_or_404(self.queryset, pk=pk)
        obj.delete()
        return reverse('pizzeria-list')

    def create(self, request):
        serializer = PizzariaDetailSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
        return reverse('pizzeria-list')


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE', ])
def pizzeria_list(request, pk=None):
    obj = Pizzeria.objects.all()

    if request.method == 'GET' and pk is not None:
        pizzeria = get_object_or_404(obj, pk=pk)
        serializer = PizzariaDetailSerializer(pizzeria)
        return JsonResponse(serializer.data, status=200)

    if request.method == 'GET':
        serializer = PizzariaListSerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PizzariaDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    if request.method == 'PUT':
        pizzeria = get_object_or_404(obj, pk=pk)
        serializer = PizzariaDetailSerializer(instance=pizzeria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    if request.method == 'DELETE':
        print('delete')
        pizzeria = get_object_or_404(obj, pk=pk)
        pizzeria.delete()
        return HttpResponse(status=204)


class PizzerriaApiView(APIView):
    queryset = Pizzeria.objects.all()

    def get_object(self, pk=None):
        try:
            return self.queryset.get(pk=pk)
        except Pizzeria.DoesNotExist:
            return Http404

    def get(self, request, pk):
        data = self.get_object(pk=pk)
        serializer = PizzariaDetailSerializer(instance=data)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = PizzariaDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions


class PizzeriaNewApi(generics.GenericAPIView,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin):
    queryset = Pizzeria.objects.all()
    serializer_class = PizzariaListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerReadOnlyPermission,
                          ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SnippetListView(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerReadOnlyPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [
        # permissions.IsAuthenticatedOrReadOnly,
        IsOwnerReadOnlyPermission,
    ]


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]


class AlbumView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class TrackView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
