import json
import dateutil.parser

from django.views.generic import DetailView, ListView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count


from django_baseline import get_or_create_csrf_token

from .models import *


@login_required
def dashboard(request):

    return render(request, 'django_simplequiz/dashboard.html', {
        'attempts': Attempt.objects.filter(user_id=request.user.id).select_related('quiz').order_by('-finished_at'),
        'challenges': Challenge.get_challenges(request.user.id)
    })


def discover(request):
    """
    Discover quizzes.
    """

    qs = Quiz.objects.filter(published=True)\
      .annotate(num_attempts=Count('attempts', distinct=True))\
      .annotate(num_likes=Count('likes', distinct=True))

    most_played = qs.order_by('-num_attempts')[:20]
    new = qs.order_by('-created_at')[:20]

    # Collect likes for all displayed quizzes to prevent extra queries.
    ids = [x.id for x in most_played] + [x.id for x in new]
    likes = QuizLike.objects.filter(user=request.user, id__in=ids).values_list('quiz_id')
    likes = [x[0] for x in likes]

    return render(request, 'django_simplequiz/discover.html', {
        'page_title': 'Discover Quizzes',
        'head_title': 'Discover Quizzes',

        'most_played': most_played,
        'new': new,

        'likes': likes,
    })


@login_required
def like(request, pk):
    result = ''

    # Check if user already likes quiz.
    if QuizLike.objects.filter(user_id=request.user.id, quiz_id=pk).count():
        result = 'already_liked'
    else:
        quiz = get_object_or_404(Quiz, pk=pk)
        like = QuizLike(quiz=quiz, user=request.user)
        like.save()

        result = 'ok'

    if request.is_ajax():
        return HttpResponse(result)
    else:
        return redirect('quiz', pk=pk)


class QuizDetailView(DetailView):

  model = Quiz
  template_name = "django_simplequiz/quiz.html"


  def dispatch(self, *args, **kwargs):
    response = super(QuizDetailView, self).dispatch(*args, **kwargs)
    if not (self.object.published or self.object.user_can_edit(self.request.user)):
        raise PermissionDenied('Unpublished!')

    return response


  def get_context_data(self, *args, **kwargs):
    context = super(QuizDetailView, self).get_context_data(*args, **kwargs)

    store = self.object.get_json_store(False)

    store['user_authenticated'] = self.request.user.is_authenticated()

    store['label_pause'] = 'Pause'
    store['label_resume'] = 'Resume'

    store['save_attempt_url'] = reverse('quiz_save_attempt')

    store['csrf'] = get_or_create_csrf_token(self.request)

    context['store'] = json.dumps(store)
    context['show_hints'] = store['show_hints']
    context['show_info'] = store['show_info']
    context['can_page'] = store['can_page']
    context['label_pause'] = 'Pause'
    context['label_resume'] = 'Resume'
    context['label_restart'] = 'Restart'

    return context





@require_http_methods(["POST"])
def save_attempt(request):
    quiz = get_object_or_404(Quiz, pk=request.POST.get('id'))

    attempt = Attempt(quiz=quiz)
    attempt.started_at = dateutil.parser.parse(request.POST.get('started_at'))
    attempt.finished_at = dateutil.parser.parse(request.POST.get('finished_at'))
    attempt.time_taken = int(float(request.POST.get('time_taken')))
    attempt.score = float(request.POST.get('score'))

    if request.user.is_authenticated:
        attempt.user = request.user

    attempt.save()

    pos, attempts = attempt.get_rank()

    personal_pos = personal_attempts = None
    if request.user.is_authenticated:
        personal_pos, personal_attempts = attempt.get_personal_rank()

    answer = {
        'success': True,
        'pos': pos,
        'attempts': attempts,
        'personal_pos': personal_pos,
        'personal_attempts': personal_attempts,
        'score': attempt.score
    }

    #import ipdb; ipdb.set_trace()

    return HttpResponse(json.dumps(answer), content_type="application/json")
