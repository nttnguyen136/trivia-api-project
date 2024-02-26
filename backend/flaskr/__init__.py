import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)


    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        return jsonify({
            'categories': formatted_categories
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]
        current_questions = formatted_questions[start:end]

        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            'questions': current_questions,
            'total_questions': len(formatted_questions),
            'categories': formatted_categories,
            'current_category': None
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)  # Question not found

            db.session.delete(question)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Question deleted successfully'
            })

        except Exception as e:
            db.session.rollback()
            abort(500)  # Internal server error

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            data = request.get_json()

            # Validate required fields
            if 'question' not in data or 'answer' not in data or 'category' not in data or 'difficulty' not in data:
                abort(400)  # Bad request

            # Create a new question
            question = Question(
                question=data['question'],
                answer=data['answer'],
                category=data['category'],
                difficulty=data['difficulty']
            )

            db.session.add(question)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Question created successfully',
                'question_id': question.id
            })

        except Exception as e:
            db.session.rollback()
            abort(500)  # Internal server error

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            data = request.get_json()

            # Validate required fields
            if 'searchTerm' not in data:
                abort(400)  # Bad request

            search_term = data['searchTerm']

            # Search for questions
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            # Serialize questions into JSON response
            questions_data = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': questions_data,
                'total_questions': len(questions_data)
            })

        except Exception as e:
            abort(500)  # Internal server error

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            abort(404)

        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': category.format()
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            data = request.get_json()

            # Validate required fields
            if 'category' not in data or 'previous_questions' not in data:
                abort(400)  # Bad request

            category = data['category']
            previous_questions = data['previous_questions']

            # Get a random question within the given category and not in previous_questions
            question = Question.query.filter(Question.category == category, ~Question.id.in_(previous_questions)).order_by(func.random()).first()

            if question is None:
                # No more questions available in the given category
                return jsonify({
                    'success': True,
                    'question': None
                })

            # Serialize question into JSON response
            question_data = question.format()

            return jsonify({
                'success': True,
                'question': question_data
            })

        except Exception as e:
            abort(500)  # Internal server error

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app

