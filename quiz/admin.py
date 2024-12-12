from django.contrib import admin
from .models import Question, Choice, Answer, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)

class ChoiceInline(admin.TabularInline):
    """
    Inline for managing choices within the question admin page.
    """
    model = Choice
    extra = 3  # Display 3 empty choice fields by default
    min_num = 1  # Require at least 1 choice
    verbose_name = "Choice"
    verbose_name_plural = "Choices"


class AnswerInline(admin.TabularInline):
    """
    Inline for managing answers within the question admin page.
    """
    model = Answer
    extra = 1  # Display 1 empty answer field by default
    min_num = 1  # Require at least 1 answer
    verbose_name = "Answer"
    verbose_name_plural = "Answers"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Question model.
    """
    list_display = ('text', 'question_type', 'category','created_at', 'updated_at')  # Fields displayed in the list view
    list_filter = ('question_type', 'created_at')  # Filters for easier navigation
    search_fields = ('text',)  # Searchable by question text
    # inlines = [ChoiceInline, AnswerInline]  # Include Choices and Answers inline for easy management


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Choice model.
    """
    list_display = ('text', 'question', 'created_at')
    list_filter = ('question',)
    search_fields = ('text', 'question__text')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Answer model.
    """
    list_display = ('question', 'choice')
    list_filter = ('question',)
    search_fields = ('question__text', 'choice__text')
