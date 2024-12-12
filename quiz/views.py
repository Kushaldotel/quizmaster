from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Question, Choice, Answer
from django.http import JsonResponse
import random
from django.core.exceptions import ValidationError


def select_category(request):
    """
    View to display all available categories.
    """
    categories = Category.objects.filter(parent=None)  # Top-level categories
    return render(request, 'quiz/select_category.html', {'categories': categories})


def start_quiz(request, category_id):
    """
    Start the quiz by fetching the first question in the selected category.
    """
    category = get_object_or_404(Category, id=category_id)
    questions = Question.objects.filter(category=category)
    if questions.exists():
        first_question = questions.first()
        return redirect('display_question', category_id=category.id)  # Just pass category_id to display questions
    return render(request, 'quiz/no_questions.html', {'category': category})


def display_question(request, category_id):
    """
    Display a set of 10 random questions from a particular category.
    Handle user's answer submission and display feedback.
    """
    category = get_object_or_404(Category, id=category_id)

    # Get random 10 questions from the selected category
    questions = Question.objects.filter(category=category)

    # If there are fewer than 10 questions, show all
    if questions.count() < 10:
        questions = questions.all()
    else:
        questions = questions.order_by('?')[:10]  # Get 10 random questions

    user_answers = {}
    correct_answers_count = 0
    incorrect_answers_count = 0

    if request.method == 'POST':
        # Collect all the answers
        for question in questions:
            user_answers[question.id] = request.POST.getlist(f'answers_{question.id}')

        # Validation for single-choice questions: ensure only one choice is selected
        for question in questions:
            if question.question_type == Question.SINGLE_CHOICE:
                if len(user_answers.get(question.id, [])) > 1:
                    return render(request, 'quiz/display_questions.html', {
                        'questions': questions,
                        'category': category,
                        'error_message': f"You can only select one answer for question: '{question.text}'"
                    })

        # Evaluate answers
        for question in questions:
            correct_choices = Answer.objects.filter(question=question)
            user_selected_choices = user_answers.get(question.id, [])

            # If the question is single-choice, check if the selected choice is correct
            if question.question_type == Question.SINGLE_CHOICE:
                if user_selected_choices and correct_choices.filter(choice_id=user_selected_choices[0]).exists():
                    correct_answers_count += 1
                else:
                    incorrect_answers_count += 1
            # If the question is multiple-choice, check if all selected choices are correct
            elif question.question_type == Question.MULTIPLE_CHOICE:
                # Get all correct choices for the question
                correct_choice_ids = set(correct_choices.values_list('choice', flat=True))

                # Get the user's selected choices
                user_selected_choices = set(map(int, user_answers.get(question.id, [])))  # Convert to set of integers

                # Check if all user's selected choices match the correct choices
                if user_selected_choices == correct_choice_ids:
                    correct_answers_count += 1
                else:
                    incorrect_answers_count += 1

        # Redirect to quiz completion page with results
        return redirect('quiz_completed', category_id=category.id, correct_answers=correct_answers_count, incorrect_answers=incorrect_answers_count)

    return render(request, 'quiz/display_questions.html', {
        'questions': questions,
        'category': category,
    })


def quiz_completed(request, category_id, correct_answers, incorrect_answers):
    """
    Display the quiz results: total correct answers, incorrect answers, and feedback.
    """
    category = get_object_or_404(Category, id=category_id)
    total_questions = correct_answers + incorrect_answers

    # Feedback based on the score
    if correct_answers == total_questions:
        feedback = "Excellent! You got all answers correct."
    elif correct_answers > incorrect_answers:
        feedback = "Good job! You got more answers correct than wrong."
    else:
        feedback = "Better luck next time! Keep practicing."

    return render(request, 'quiz/quiz_completed.html', {
        'category': category,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'feedback': feedback,
    })

