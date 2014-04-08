from django.conf.urls import patterns, include, url

from .views import *


urlpatterns = patterns('django_simplequiz.views',
    # url(r'^$', 'medbase.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^dashboard$', 'dashboard', name="quiz_dashboard"),
    url(r'^discover$', 'discover', name="simplequiz_discover"),

    url(r'^quiz-attempt/save$', 'save_attempt', name="quiz_save_attempt"),
    #url(r'^quiz/(?P<pk>\d+)/my-attempts$', AttemptListView.as_view(), name="quiz_attempts"),

    url(r'^quiz/(?P<pk>\d+)$', QuizDetailView.as_view(), name='quiz'),
    url(r'^quiz/(?P<slug>[-_\w]+)$', QuizDetailView.as_view(), name='quiz_slugged'),

    url(r'^quiz/(?P<pk>\d+)/like$', 'like', name='simplequiz_like'),
)
