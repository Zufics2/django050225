from django.urls import path
from django.urls import re_path
from django.views.generic import CreateView
from bboard.models import Bb

from bboard.views import (by_rubric, BbCreateView, add, add_save, add_and_save, bb_detail, logging_check, no_login,
                          BbRubricBbsView, IndexView, BbDetailView, BbDeleteView, FirstUserView, index, api_rubric,
                          api_rubric_detail, api_create_user)

app_name = 'bboard'

urlpatterns = [
    ### DRF ###
    path('api/v1/rubrics/<int:pk>/', api_rubric_detail),
    path('api/v1/rubrics/', api_rubric),
    #PR 30.03.26
    path('api/v1/users/', api_create_user),

    path('add/', BbCreateView.as_view(), name='add'),

    # path('add/', add, name='add'),
    # path('add/save/', add_save, name='add_save'),
    # path('add/', add_and_save, name='add'),
    # path('add/', CreateView.as_view(model=Bb, template_name='create.html', fields='__all__'),name='add'),

    # path('rubric/<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('rubric/<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),
    # path('bb/<int:bb_id>/', bb_detail, name='bb_detail'),
    path('bb/<int:pk>/', BbDetailView.as_view(), name='bb_detail'),

    path('bb/delete/<int:pk>/', BbDeleteView.as_view(), name='bb_delete'),

    path('logging/', logging_check, name='logging_check'),
    path('no_login/', no_login, name='no_login'),
    path('', index, name='index'),


    # path('', index, name='index'),
    # path('', IndexView.as_view(), name='index'),

    #PR 12.03.26
    path('user/', FirstUserView.as_view(), name='first_user')

    #dz

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