"""blog databse field..."""
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class PublishedManager(models.Manager):
    """custmize object ..."""

    def get_queryset(self):
        """Query set in user manager.."""
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    """Post class model..."""

    choice = (
             ('draft', 'Draft'),
             ('published', 'Published'),)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=choice,
                              default='draft')

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom  manager.

    class Meta:
        """meta class of Post model.."""

        ordering = ('-publish',)

    def __str__(self):
        """Return object name in user readable.."""
        return self.title

    def get_absolute_url(self):
        """Canonical URLs for models.."""
        return reverse("blog:post_detail", args=[self.publish.year,
                       self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    """comment on the post model.."""

    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=255)
    body = models.TextField(null=True,blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        """meta class for ordering..."""

        ordering = ('created',)

    def __str__(self):
        """Return object name humane readble form..."""
        return "Comment by{} on {}".format(self.name, self.post)
