from django.urls import path
from django.urls import re_path

from bboard.views import (index, by_rubric, BbCreateView, add, add_save, add_and_save, sms_list)

app_name = 'bboard'

urlpatterns = [
    # path('add/', BbCreateView.as_view(), name='add'),

    # path('add/', add, name='add'),
    # path('add/save/', add_save, name='add_save'),
    path('add/', add_and_save, name='add'),

    path('<int:rubric_id>/', by_rubric, name='by_rubric'),

    path('', index, name='index'),

    #dz
    path("sms/", sms_list, name="sms_list")

    # practice
    # path('comments/', get_comments, name="get_comments"),
    # path('comment/out', comments_out, name="comments_out"),
    # path('comments/delete/<int:sms_id>/', delete_comments, name="delete_comments")
]

# url_patterns = [
#     re_path(r'^add/$', BbCreateView.as_view(), name='add'),
#     re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, name='by_rubric'),
#     re_path(r'^$', index, name='index'),
# ]