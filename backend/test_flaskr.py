import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from setting import DB_PASSWORD, DB_USER, DB_HOST, DB_PORT, DB_NAME
from flaskr import create_app
from models import Question, setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME
        self.database_path = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Test data
        self.question_create_data = {
            "question": "What boxer's original name is Cassius Clay?",
            "category": 3,
            "difficulty": 2,
            "answer": "Tom Cruise",
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))

    def test_invalid_page_returns_404(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    def test_delete_question(self):
        res = self.client().delete("/questions/2")
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], "Question 2 deleted successfully")
        self.assertEqual(question, None)

    def test_delete_question_invalid_id(self):
        res = self.client().delete("/questions/222")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    def test_create_question(self):
        res = self.client().post(
            "/questions",
            json=self.question_create_data,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], "Question created successfully")

    def test_create_question_fail(self):
        res = self.client().post(
            "/questions",
            json={},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")

    def test_search_question(self):
        res = self.client().post("/questions/search", json={"searchTerm": "title"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue((data["total_questions"]))

    def test_search_question_fail(self):
        res = self.client().post("/questions/search", json={})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")

    def test_get_categories_by_category(self):
        res = self.client().get("/categories/1/questions")

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue((data["total_questions"]))
        self.assertTrue((data["current_category"]))

    def test_get_categories_by_category_invalidId(self):
        res = self.client().get("/categories/999/questions")

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    def test_play_quiz(self):
        res = self.client().post(
            "/quizzes", json={"category": 3, "previous_questions": []}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_play_quiz_not_category(self):
        res = self.client().post(
            "/quizzes", json={"category": 9999, "previous_questions": []}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"], None)

    def test_play_quiz_400(self):
        res = self.client().post("/quizzes", json={})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
