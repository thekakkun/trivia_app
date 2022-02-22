import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.user = 'postgres'
        self.password = 'abc'
        self.host = 'localhost'
        self.port = '5432'
        self.database_name = "trivia_test"
        self.database_path = f'postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    @TODO:
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['categories']), 6)

    def test_post_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(data['code'], 405)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertIsNone(data['current_category'])
        self.assertTrue(data['categories'])

    def test_get_big_page(self):
        res = self.client().get('/questions?page=99999')
        data = json.loads(res.data)
        self.assertEqual(data['code'], 404)

    def test_add_question(self):
        new_question = {
            'question': 'What is the largest mammal?',
            'answer': 'Blue whale',
            'category': 1,
            'difficulty': 2
        }
        res = self.client().post('/questions', json=new_question)
        self.assertEqual(res.status_code, 200)

    def test_delete_question(self):
        questions = Question.query.order_by(Question.id.desc())
        question_count = questions.count()
        res = self.client().delete(f'/questions/{questions.first().id}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Question.query.count(), question_count-1)

    def test_delete_non_existant_question(self):
        res = self.client().delete('/questions/99999')
        self.assertEqual(res.status_code, 404)

    def test_get_questions_in_cat(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'Science')
        self.assertTrue(data['categories'])

    def test_get_non_existant_category(self):
        res = self.client().get('/categories/99999/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_start_quiz(self):
        req = {
            'quiz_category': {'id': '2', 'type': 'Art'},
            'previous_questions': [16, 17, 18]
        }
        res = self.client().post('/quizzes', json=req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue('answer' in data['question'])
        self.assertTrue('category' in data['question'])
        self.assertTrue('difficulty' in data['question'])
        self.assertTrue('id' in data['question'])
        self.assertTrue('question' in data['question'])

    def test_end_quiz(self):
        req = {
            'quiz_category': {'id': '2', 'type': 'Art'},
            'previous_questions': [16, 17, 18, 19]
        }
        res = self.client().post('/quizzes', json=req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
