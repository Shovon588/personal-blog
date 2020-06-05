from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Story(models.Model):
    """
    Creates a story for writing multiple post in it. The story can be treated as a folder.
    The folder can contain multiple episodes in it. A story uses user information as a foreign
    key and also a story name, story trailer to have some glance about the story and a creation
    date.
    """
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    story_name = models.CharField(max_length=256)
    story_trailer = models.TextField(blank=True)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.story_name


class Post(models.Model):
    """
    Under the story folder a story can have multiple posts. This model creates those individual
    posts. It creates an instance after every creation of a post. The model takes some required
    parameters such as story as a foreign key, a title, the full post and date. The story needs
    to publish before finally going live.
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(null=True, blank=True)

    def publish(self):
        """
        If the author hit publish, this function will update the value of published date.
        Hence the post will be published.
        """
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        """
        This function will approve the comments by the author.
        """
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    The users can add a comment to any post. Upon commenting this model will create a new
    entry to the database having the following information.
    """
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=150)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        """
        Like the post a comment needs to be approved by the author as well. This function
        does so.
        """
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text


class About(models.Model):
    """
    Some info about the author or the blog.
    """
    about = models.TextField()

    def __str__(self):
        return self.about


class ReaderInfo(models.Model):
    """
    This model will create an entry when a user reads a particular post. This will store user
    ip, which post they are reading and the time of the read. With this we can retrieve the
    favourite time among the readers, who is visiting the page often, which blog is read how many
    times etc.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='readerinfos')
    user_ip = models.CharField(max_length=100, unique=False)
    read_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s at %s" %(self.user_ip, self.read_time)