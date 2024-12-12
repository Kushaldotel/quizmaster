### README for Quiz Application


## Project Overview
This is a Django-based quiz application that allows users to take quizzes categorized by topics. Each quiz consists of questions with multiple-choice or single-choice answers. The application evaluates user responses and provides feedback upon quiz completion.


## Features
- Categories: Organizes questions by topic.
- Randomized Questions: Displays a set of 10 random questions per quiz.
- Single & Multiple Choice Questions: Supports both types of questions.
- Answer Evaluation: Validates user responses against correct answers.
- Feedback: Provides feedback and results at the end of the quiz.



## Setup Instructions

### Prerequisites
1. Python (>= 3.8)
2. Django (>= 3.2)
3. PostgreSQL (Optional but recommended)

### Installation
1. Clone the repository:
   git clone https://github.com/Kushaldotel/quizmaster.git
   cd QuizMaster

2. Create a virtual environment:
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Set up the database:
   Update the `DATABASES` configuration in `settings.py` if using PostgreSQL or another database.

   Apply migrations:
   python manage.py makemigrations
   python manage.py migrate

   I have already pushed a dbsqlite3 you can use the existing data too.
   Admin username: admin
   Admin password: P@55word

5. Create a superuser:
   python manage.py createsuperuser


6. Run the server:
   python manage.py runserver

7. Access the application at `http://127.0.0.1:8000`.


## Models and Assumptions

### 1. Category Model
- Represents the topic of a quiz (e.g., Science, Math).
- Fields:
  - `name`: Name of the category.
  - `description`: A brief description of the category.

### 2. Question Model
- Represents a question in the quiz.
- Fields:
  - `text`: The question text.
  - `category`: ForeignKey to the `Category` model.
  - `question_type`: Type of question (`SC` for single-choice, `MC` for multiple-choice).

### 3. Choice Model
- Represents possible answers for a question.
- Fields:
  - `text`: The choice text.
  - `question`: ForeignKey to the `Question` model.

### 4. Answer Model
- Represents the correct answer(s) for a question.
- Fields:
  - `question`: ForeignKey to the `Question` model.
  - `choice`: ForeignKey to the `Choice` model.



## Key Assumptions
1. Categories:
   - Quizzes are grouped by categories. Each category can have multiple questions.

2. Questions:
   - Each question belongs to a single category.
   - Question types are either:
     - Single-choice (`SC`): One correct answer.
     - Multiple-choice (`MC`): Multiple correct answers.

3. Choices:
   - Each question has multiple choices, but the correct ones are stored in the `Answer` model.

4. Answers:
   - The `Answer` model links correct choices to their respective questions.


## Workflow

### 1. Taking a Quiz
- The user selects a category to start a quiz.
- A set of 10 random questions from the selected category is displayed.
- Questions may include:
  - Single-choice questions: Users can select only one option.
  - Multiple-choice questions: Users can select multiple options.

### 2. Submitting Answers
- User answers are submitted via a POST request.
- The server evaluates answers against the `Answer` model.

### 3. Evaluating Answers
- For single-choice questions:
  - The selected choice is validated against the `Answer` model.
- For multiple-choice questions:
  - All selected choices are compared to the correct choices stored in the `Answer` model.
  - If all match, the answer is marked correct.

### 4. Results and Feedback
- After submission, the user is redirected to the results page.
- Results include:
  - Total correct answers.
  - Total incorrect answers.
  - Feedback (e.g., "Excellent", "Good job", etc.).


## Enhancements
- Add authentication for personalized quiz history.
- Store results in the database for analytics.
- Add a timer for quizzes.
- Enable the addition of images or media in questions.



Feel free to modify the content to suit your use case or contribute to the project!