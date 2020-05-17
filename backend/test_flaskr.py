import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=100000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
    
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
    
    def test_delete_question(self):
        res = self.client().delete('/questions/25')
        data = json.loads(res.data)

        question = Question.query.get(25)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(question, None)
    
    def test_404_delete_non_exist_question(self):
        res = self.client().delete('/questions/1000000000')
        data = json.loads(res.data)

        question = Question.query.get(1000000000)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_add_question(self):
        body = {
            'question': 'question',
            'answer': 'answer',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions',json=body)
        data = json.loads(res.data)
        q = Question.query.order_by(desc(Question.id)).first()
        id = q.id
        message = str(id) + " added"
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], message)
    
    def test_422_add_question(self):
        body = {
            'answer': 'answer',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions',json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    def test_search_question(self):
        body = {
            'searchTerm': 'what'
        }
        res = self.client().post('/questions/search',json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])

    def test_404_get_non_exist_search_question(self):
        body = {
            'searchTerm': 'This term is not exist'
        }
        res = self.client().post('/questions/search',json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'],'resource not found')
    
    def test_get_category_questions(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        category = Category.query.get(2)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['category_name'],category.type)

    def test_404_get_non_exist_category_questions(self):
        res = self.client().get('/categories/5555555/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'],'resource not found')
    
    def test_quizzes(self):
        body = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Entertainment',
                'id': 5
            }
        }
        res = self.client().post('/quizzes',json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['question'])
    
    def test_quizzes(self):
        body = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Art',
                'id': 2
            }
        }
        res = self.client().post('/quizzes',json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['question'])
    
    def test_quizzes_all_categories(self):
        body = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'click',
            }
        }
        res = self.client().post('/quizzes',json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['question'])

    def test_422_quizzes(self):
        body = {
            'quiz_category': {
                'type': 'Art',
                'id': 5
            }
        }
        res = self.client().post('/quizzes',json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'],'resource not found')
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()