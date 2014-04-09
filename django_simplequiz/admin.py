from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import *

#############
# Category #
#############

admin.site.register(Category, MPTTModelAdmin)

########
# Quiz #
########

class QuestionInline(admin.TabularInline):
  model = Question


class QuizAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': ('title', 'slug', 'description', 'info', 'category', 'tags'),
    }),
    ('Settings', {
      'fields':  ('mode', 'time', 'end_on_wrong_answers', 'force_order', 
                  'allow_paging', 'randomize_order', 'one_by_one',
                  'ignore_case', 'ignore_spaces', 'auto_accept',
                  'show_answers_on_finish', 'move_answered_to_bottom', 'move_active_to_top'),
    }),
    ('Publishing', {
      'fields': ('published',)
    })
  )
  prepopulated_fields = {'slug': ('title',)}

  inlines = [QuestionInline]


  def save_model(self, request, obj, form, change):
    if not obj.pk:
      obj.created_by = request.user

    obj.save()

admin.site.register(Quiz, QuizAdmin)

#############
# Complaint #
#############

class ComplaintAdmin(admin.ModelAdmin):
  readonly_fields = ('quiz', 'subject', 'message', 'email', 'user')
  list_display = ('subject', 'quiz', 'user', 'handled')

admin.site.register(Complaint, ComplaintAdmin)
