from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import db, setup_db, Question, Category
import random

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )

        return response

    # Get a list of categories.
    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories = Category.query.all()

        if not categories:
            abort(404)

        formatted_categories = [category.format() for category in categories]

        return jsonify({"success": True, "categories": formatted_categories})

    # Get a list of questions.
    @app.route("/questions", methods=["GET"])
    def get_questions():
        page = request.args.get("page", 1, type=int)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]
        current_questions = formatted_questions[start:end]

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(formatted_questions),
                "categories": formatted_categories,
                "current_category": None,
            }
        )

    # Delete a question by question id
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):

        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)  # Question not found

        try:

            db.session.delete(question)
            db.session.commit()

            return jsonify(
                {"success": True, "message": "Question deleted successfully"}
            )

        except Exception as e:
            db.session.rollback()
            abort(500)  # Internal server error

    # Create a question
    @app.route("/questions", methods=["POST"])
    def create_question():
        data = request.get_json()

        # Validate required fields
        if (
            "question" not in data
            or "answer" not in data
            or "category" not in data
            or "difficulty" not in data
        ):
            abort(400)  # Bad request

        try:

            # Create a new question
            question = Question(
                question=data["question"],
                answer=data["answer"],
                category=data["category"],
                difficulty=data["difficulty"],
            )

            db.session.add(question)
            db.session.commit()

            return jsonify(
                {
                    "success": True,
                    "message": "Question created successfully",
                    "question_id": question.id,
                }
            )

        except Exception as e:
            db.session.rollback()
            abort(500)  # Internal server error

    # Search question
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        try:
            data = request.get_json()

            # Validate required fields
            if "searchTerm" not in data:
                abort(400)  # Bad request

            search_term = data["searchTerm"]

            # Search for questions
            questions = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")
            ).all()

            # Serialize questions into JSON response
            questions_data = [question.format() for question in questions]

            return jsonify(
                {
                    "success": True,
                    "questions": questions_data,
                    "total_questions": len(questions_data),
                }
            )

        except Exception as e:
            abort(500)  # Internal server error

    # Get questions by category
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            abort(404)

        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify(
            {
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(formatted_questions),
                "current_category": category.format(),
            }
        )

    # Get quizzes by category and previous questions
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        data = request.get_json()

        # Validate required fields
        if "category" not in data or "previous_questions" not in data:
            abort(400)  # Bad request

        category = data["category"]
        previous_questions = data["previous_questions"]

        try:

            questions = Question.query.filter(
                Question.category == category, ~Question.id.in_(previous_questions)
            ).all()

            if len(questions) == 0:
                return jsonify({"success": True, "question": None})

            question = random.choice(questions)
            return jsonify({"success": True, "question": question.format()})

        except Exception as e:
            abort(500)  # Internal server error

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not Found"}), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "Unprocessable Entity"}
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal Server Error"}
            ),
            500,
        )

    return app
