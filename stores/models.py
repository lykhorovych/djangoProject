from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


# Create your models here.
class Pizzeria(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=400, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip_code = models.IntegerField(max_length=5, blank=True, default=0)
    website = models.URLField(blank=True, max_length=420)
    phone_number = models.IntegerField(max_length=10,
                                       blank=True,
                                       validators=[RegexValidator(regex=r'^\d{9,10}$'), ])
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True,
                              upload_to='pizzariaImages',
                              default='pizzariaImages/pizzalogo.png')
    email = models.EmailField(max_length=245, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ' ' + self.city


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=10, default="", blank=True)
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, default='python')
    style = models.CharField(max_length=100, choices=STYLE_CHOICES, default='friendly')
    owner = models.ForeignKey(User, related_name='snippets', on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.code


class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)


class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ['album', 'order', ]
        ordering = ['order', ]

    def __str__(self):
        return str(self.order) + " " + self.title

