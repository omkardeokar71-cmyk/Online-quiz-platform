from django.test import TestCase
from django.contrib.auth.models import User
from .models import Quiz

class QuizModelTest(TestCase):
    def test_create_quiz(self):
        user = User.objects.create(username="testuser")
        quiz = Quiz.objects.create(
            title="Test Quiz",
            description="Test Desc",
            created_by=user
        )
        self.assertEqual(quiz.title, "Test Quiz")
# Create your tests here.
