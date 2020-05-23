from django.contrib import admin
from .models import Post,Comment, About, Story, ReaderInfo

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(About)
admin.site.register(Story)
admin.site.register(ReaderInfo)

