from django.db import models
from django.contrib.auth.models import User

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # if self.slug == '':
        #     self.slug = '-'.join(str(self.title).split())

        # this runs at saves and updates
        self.slug = '-'.join(str(self.title).split())

        i = super(Post, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        return i
