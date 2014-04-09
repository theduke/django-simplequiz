import json

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
from django.core.exceptions import ValidationError

from django.db.models import Q

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):

  name = models.CharField(max_length=100, unique=True)
  description = models.TextField(blank=True)

  parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

  class Meta:
    verbose_name_plural = "Categories"

  class MPTTMeta:
      order_insertion_by = ['name']


  def __unicode__(self):
    return self.name


class Quiz(models.Model):

  MODE_TYPE = "type"
  MODE_CLICK = "click"

  MODE_CHOICES = (
    (MODE_TYPE, 'Typing'),
    (MODE_CLICK, 'Clicking')
  )

  title = models.CharField(max_length=80, unique=True)
  slug = models.SlugField(max_length=255, unique=True)
  description = models.TextField(blank=True)
  info = models.TextField(blank=True, help_text='Info that will only be shown once the user has finished the Quiz. Only shown on fail if show ansers on finish is enabled.')
  tags = TaggableManager(blank=True)
  category = models.ForeignKey(Category, null=True, blank=True)

  mode = models.CharField(max_length=50, choices=MODE_CHOICES)
  time = models.PositiveIntegerField(help_text='How long does a user have time to answer? (SECONDS)')

  end_on_wrong_answers = models.PositiveIntegerField(default=0, help_text='If greater than 0, the quiz will fail if the user gives as many wrong answers as specified.')

  force_order = models.BooleanField(default=False, help_text='Force the questions the be asked in a fixed order.')
  allow_paging = models.BooleanField(default=True, help_text='Allow the user to switch between questions (Only relevant if "Force order" is enabled).')
  randomize_order = models.BooleanField(default=False, help_text='Show questions or hints in a random order.')
  one_by_one = models.BooleanField(default=False, help_text='If enabled, only one question is shown at a time. Otherwise, all questions are shown at one. (No effect for clickable quiz)')

  move_answered_to_bottom = models.BooleanField(default=False, help_text='Move an answered item to the bottom of the question to list to make it easier to see the unanswered ones. Useful for long lists. Has no effect in one by one mode!')
  move_active_to_top = models.BooleanField(default=False, help_text='Move the active question to the top of the question/answer list. Makes it easy to spot the active question on long lists. Has no effect in click mode or for one by one.')

  ignore_case = models.BooleanField(default=True, help_text='Ignore the case of answers.')
  ignore_spaces = models.BooleanField(default=True, help_text='Ignore spaces in answers.')
  auto_accept = models.BooleanField(default=True, help_text='Only for TYPING: If enabled, a typed answer that is correct is automatically accepted. Otherwise, the user has to confirm with enter.')

  show_answers_on_finish = models.BooleanField(default=True, help_text='If disabled, the user will not see the correct answers for the questions that were not answered correctly.')

  published = models.BooleanField(default=False)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_by = models.ForeignKey(User, null=True, blank=True, related_name='+')

  playcount = models.PositiveIntegerField(default=0)


  class Meta:
    verbose_name_plural = "Quizzes"


  def __unicode__(self):
    return self.title


  def user_can_edit(self, user):
    return user.is_superuser or self.created_by == user


  def clean(self):
    pass


  def show_hints(self, questions=None):
    if not questions:
      questions = self.questions.all()

    return bool(len([x.name for x in questions if x.name]))

  def show_info(self, questions=None):
    if not questions:
      questions = self.questions.all()

    return bool(len([x.info for x in questions if x.info]))


  def get_json_store(self, as_string=True):
    questions = self.get_questions()

    store = {
      'id': self.id,
      'title': escape(self.title),
      'description': escape(self.description),
      'info': escape(self.info),
      'mode': self.mode,
      'time': self.time,
      'end_on_wrong_answers': self.end_on_wrong_answers,
      'force_order': self.force_order,
      'allow_paging': self.allow_paging,
      'randomize_order': self.randomize_order,
      'one_by_one': self.one_by_one,
      'ignore_case': self.ignore_case,
      'ignore_spaces': self.ignore_spaces,
      'auto_accept': self.auto_accept,
      'move_answered_to_bottom': self.move_answered_to_bottom,
      'move_active_to_top': self.move_active_to_top,

      'show_answers_on_finish': self.show_answers_on_finish,

      'show_hints': self.show_hints(questions),
      'show_info': self.show_info(questions),

      'can_page': (self.force_order or self.one_by_one or self.mode == self.MODE_CLICK) and self.allow_paging,

      'questions': [q.get_json_store() for q in self.get_questions()],
    }

    return json.dumps(store) if as_string else store

  def get_questions(self):
    order = '?' if self.randomize_order else 'weight'
    return self.questions.all().order_by(order)


class Question(models.Model):

  KIND_PLAIN = 'plain'
  KIND_MULTIPLE_CHOICE = 'multiple_choice'
  KIND_SINGLE_CHOICE = 'single_choice'

  KIND_CHOICES = (
    (KIND_PLAIN, 'Plain'),
    (KIND_MULTIPLE_CHOICE, 'Multiple choice'),
    (KIND_SINGLE_CHOICE, 'Single choice'),
  )

  quiz = models.ForeignKey(Quiz, related_name='questions')

  kind = models.CharField(max_length=50, choices=KIND_CHOICES, default=KIND_PLAIN)

  name = models.TextField(verbose_name='Question/Hint', blank=True)
  answer = models.TextField(blank=True)
  info = models.TextField(blank=True)

  image = models.ImageField(max_length=255, blank=True, upload_to="simplequiz", help_text='Image answer for a question.')

  weight = models.IntegerField(default=0)


  def __unicode__(self):
    return self.name


  def clean(self):
    if not (self.answer or self.image):
      raise ValidationError("Either answer or file have to be specified.")


  def get_answer(self):
    return []


  def get_json_store(self):
    store = {
      'id': self.id,
      'name': escape(self.name),
      'answer': escape(self.answer),
      'image': str(self.image) if self.image else '',
      'info': escape(self.info),
      'weight': self.weight
    }
    
    return store


class Attempt(models.Model):
  user = models.ForeignKey(User, related_name='+', null=True, blank=True)
  quiz = models.ForeignKey(Quiz, related_name='attempts')

  started_at = models.DateTimeField()
  finished_at = models.DateTimeField()
  time_taken = models.PositiveIntegerField()
  score = models.FloatField(help_text='Score in percent')
  right_answers = models.PositiveIntegerField()
  mistakes = models.PositiveIntegerField()


  def verbose_score(self):
    return self.score * 100 + '%'


  def get_rank(self):
    attempts = self.quiz.attempts.all()
    count = attempts.count()

    pos = None
    if not self.score:
      pos = count
    else:
      better_scores = attempts.filter(score__gt=self.score).count()
      better_times = attempts.filter(score=self.score, time_taken__lt=self.time_taken).count()

      pos = better_scores + better_times + 1

    return (pos, count)


  def get_personal_rank(self):
    attempts = self.quiz.attempts.filter(user_id=self.user_id)
    count = attempts.count()

    pos = None
    if not self.score:
      pos = count
    else:
      better_scores = attempts.filter(score__gt=self.score).count()
      better_times = attempts.filter(score=self.score, time_taken__lt=self.time_taken).count()

      pos = better_scores + better_times + 1

    return (pos, count)


class Challenge(models.Model):

  challenger = models.ForeignKey(User, related_name='+')
  challenger_attempt = models.ForeignKey(Attempt, null=True, blank=True, related_name='+')

  challenged = models.ForeignKey(User, related_name='+')
  challenged_attempt = models.ForeignKey(Attempt, null=True, blank=True, related_name='+')

  challenged_at = models.DateTimeField(auto_now_add=True)

  declined = models.BooleanField(default=False)


  @classmethod
  def get_challenges(cls, user_id):
    return cls.objects.filter(Q(challenger_id=user_id) | Q(challenged_id=user_id)).order_by('-challenged_at')


class QuizLike(models.Model):
  quiz = models.ForeignKey(Quiz, related_name='likes')
  user = models.ForeignKey(User, related_name='+')
  time = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = (('quiz', 'user'),)
