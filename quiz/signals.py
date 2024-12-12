from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Question, Answer


@receiver(post_save, sender=Answer)
def validate_single_choice_answers(sender, instance, **kwargs):
    """
    Validates that a question of type SINGLE_CHOICE doesn't have multiple answers.
    """
    question = instance.question

    if question.question_type == Question.SINGLE_CHOICE:
        # Count the number of answers for the question
        answer_count = Answer.objects.filter(question=question).count()

        if answer_count > 1:
            raise ValidationError("Question type 'Single Choice' cannot have multiple answers.")
