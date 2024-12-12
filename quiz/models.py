from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    """
    Represents a category or subcategory for questions.
    """
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"  # Display parent > child structure
        return self.name

class Question(models.Model):
    SINGLE_CHOICE = 'SC'
    MULTIPLE_CHOICE = 'MC'
    QUESTION_TYPES = [
        (SINGLE_CHOICE, 'Single Choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
    ]

    text = models.TextField()  # The question text
    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPES,
        default=SINGLE_CHOICE
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)  # When the question was created
    updated_at = models.DateTimeField(auto_now=True)  # When the question was last updated

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)  # Choice text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} (Question: {self.question.id})"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='answers')

    def clean(self):
        """
        Ensures single-choice questions don't have multiple answers.
        """
        if self.question.question_type == Question.SINGLE_CHOICE:
            # Check if there's already an answer for this question
            existing_answers = Answer.objects.filter(question=self.question)
            if self.pk:  # Exclude the current instance if editing
                existing_answers = existing_answers.exclude(pk=self.pk)
            if existing_answers.exists():
                raise ValidationError("Single-choice questions can only have one answer.")

    def save(self, *args, **kwargs):
        """
        Override the save method to call clean for validation.
        """
        self.clean()  # Call the clean method for validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Answer for Question {self.question.id}: {self.choice.text}"