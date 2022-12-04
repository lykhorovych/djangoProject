from datetime import datetime

from rest_framework import serializers
from rest_framework.reverse import reverse
from stores.models import Pizzeria, Snippet, Album, Track
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User


class PizzariaListSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Pizzeria
        fields = [
            'id',
            'name',
            'city',
            'zip_code',
            'absolute_url',
        ]

    def get_absolute_url(self, obj):
        return reverse('detail', args=(obj.pk,))


class PizzariaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizzeria
        fields = [
            'id',
            'image',
            'name',
            'street',
            'city',
            'state',
            'website',
            'zip_code',
            'phone_number',
            'description',
            'email',
            'is_active',
        ]


class SnippetSerializer(serializers.ModelSerializer,
                        # serializers.HyperlinkedModelSerializer
                        ):
    owner = serializers.ReadOnlyField(source='owner.username')

    # highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username',
                  'snippets',
                  ]


class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

    def __str__(self):
        return f"Comment <{self.email} -- {self.content} --{self.created}"


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=100)
    created = serializers.DateTimeField()


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']

    def create(self, validated_data):
        tracks = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data, tracks=tracks)
        return album
if __name__ == '__main__':
    comment = Comment(email='lykhorovych@gmail.com', content='dsekrmker')
    serializer = CommentSerializer(comment)
    print(serializer.data)
