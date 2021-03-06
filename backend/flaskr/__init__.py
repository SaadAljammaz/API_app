import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  try:
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions
  except:
    abort(404)

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    try:
      categories = Category.query.all()
      return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in categories}
      })
    except:
      abort(404)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    try:
      allQuestions = Question.query.all()
      questions = paginate_questions(request,allQuestions)
      category = Category.query.all()
      if len(questions) == 0:
        abort(404)
      categories = []
      for i in category:
        categories.append(i.type)
      current_category = None
      number_of_total_questions = len(allQuestions)
      return jsonify({
        'success': True,
        'total_questions': number_of_total_questions,
        'current_category': current_category,
        'categories': categories,
        'questions': questions
      })
    except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      # print(question_id)
      Question.query.get(question_id).delete()
      return jsonify({
        'success': True,
      })
    except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    try:
      body = request.get_json()
      question = Question(question=body['question'],answer=body['answer'],difficulty=body['difficulty'],category=body['category'])
      question.insert()
      message = str(question.id) + " added"
      return jsonify({
        'success': True,
        'message': message
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    try:
      body = request.get_json()
      allQuestions = Question.query.filter(Question.question.ilike(f'%{body["searchTerm"]}%')).all()
      if not body["searchTerm"] or not allQuestions:
        abort(404)
      return jsonify({
        'success': True,
        'questions': [question.format() for question in allQuestions],
      })
    except:
      abort(404)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category>/questions')
  def get_category_questions(category):
    try:
      newCategory = Category.query.get(category)
      allQuestions = Question.query.filter_by(category = category).all()
      return jsonify({
        'success': True,
        'questions': [question.format() for question in allQuestions],
        'category_name': newCategory.type
      })
    except:
      abort(404)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def quizzes():
    try:
      body = request.get_json()
      quiz_category = body['quiz_category']
      previous_questions = body.get('previous_questions')

      if quiz_category['type'] == 'click':
        question2 = Question.query.filter(Question.id.notin_((previous_questions))).all()
      else:
        question = Question.query.filter_by(category=quiz_category['id'])
        question2 = question.filter(Question.id.notin_((previous_questions))).all()

      if len(question2) == 0:
        newQuestions = None
      else:
        newQuestions = question2[0].format()
      return jsonify({
        'success': True,
        'question': newQuestions
      })
    except:
      abort(404)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
    
  @app.errorhandler(500)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "Internal Server Error"
      }), 500
  
  return app

    