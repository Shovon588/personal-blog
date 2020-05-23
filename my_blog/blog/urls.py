from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutDetailView.as_view(), name='about'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/<int:pk>/', views.create_post, name='post_new'),
    path('post/<int:pk>/edit/', views.post_update_view, name='post_edit'),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    path('drafts/', views.draft_list_view, name='post_draft_list'),
    path('draft/<int:pk>/', views.draft_detail_view, name='draft_detail'),
    path('post/<int:pk>/comment', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('post/<int:pk>/publish', views.post_publish, name='post_publish'),
    path('instructions/', views.InstructionsView.as_view(), name='instructions'),
    path('stories/', views.StoryListView.as_view(), name='stories'),
    path('story_parts/<int:pk>/', views.story_part_list_view, name='story_parts'),
    path('new_story/', views.create_new_story, name='new_story'),
    path('delete_story/<int:pk>/', views.StoryDeleteView.as_view(), name='delete_story'),
    path('update_story/<int:pk>/', views.story_update_view, name='update_story'),
]