import json
import os
import random
from http.client import HTTPException

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10


def paginate(items, args):
    page = args.get('page', 1, type=int)

    page_start = (page-1) * QUESTIONS_PER_PAGE
    page_end = page_start + QUESTIONS_PER_PAGE

    return items[page_start:page_end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, origins="*")

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            return jsonify({
                'success': True,
                'categories': {str(cat.id): cat.type
                               for cat in Category.query.all()}
            })

        except:
            abort(422)

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
        all_questions = Question.query.order_by('id').all()

        try:
            questions = paginate(all_questions, request.args)

            if not questions:
                abort(404)

            return jsonify({
                'succcess': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(all_questions),
                'current_category': None,
                'categories': {str(cat.id): cat.type
                               for cat in Category.query.all()}
            })

        except Exception as e:
            abort(e.code) if e.code else abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['GET'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)

            if not question:
                abort(404)
            else:
                question.delete()
                return get_questions()

        except Exception as e:
            abort(e.code) if e.code else abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            content = request.json
            if 'searchTerm' in content:
                term = content.get('searchTerm')
                matching_questions = Question.query.filter(
                    Question.question.ilike(f'%{term}%')).all()
                questions = paginate(matching_questions, request.args)

                return jsonify({
                    'succcess': True,
                    'questions': [question.format() for question in questions],
                    'total_questions': len(matching_questions),
                    'current_category': None,
                    'categories': {str(cat.id): cat.type
                               for cat in Category.query.all()}
                })

            else:
                question = Question(**content)
                question.insert()

                return get_questions()

        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def get_cat_questions(cat_id):
        try:
            matching_questions = Question.query.filter(
                Question.category == cat_id).all()
            questions = paginate(matching_questions, request.args)

            return jsonify({
                'succcess': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(matching_questions),
                'current_category': Category.query.get(cat_id).type,
                'categories': {str(cat.id): cat.type
                               for cat in Category.query.all()}

            })

        except:
            abort(422)

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

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
