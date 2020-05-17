# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT

URI|Method|Explanation|Return example|Curl example
--- | --- | --- | ---| ---
`/categories`|GET| Retrive a List of all categories including its id and name|`{'success': <Bool>, 'categories': [<int,String>]}`|`curl http://127.0.0.1:5000/categories`
`/questions`|GET| Retrive paginated questions (10 per page) as a List including total number of questions, current_category and all categories, | `{'success': <Bool>, 'total_questions': <int>, 'current_category': 'None','categories': [<String>],'questions': [<obj>]}`|`curl http://127.0.0.1:5000/questions`
`/questions/<int:question_id>`|DELETE| Deletes the selected questions by id|`{'success': <Bool>}`|`curl http://127.0.0.1:5000/questions/2 -X DELETE`
`/add`|POST| Adds a new question to the database|`{'success': <Bool>, 'message': <String>}`|`curl http://127.0.0.1:5000/add -X POST -H"Content-Type: application/json" -d"{'question':"question", 'answer': "answer"}, 'difficulty': <str>,'category':<str/int>}"`
`/questions/search`|POST| Searches for a string on all the questions.|`{'success': <Bool>, 'questions': [<obj>]}`|`curl http://127.0.0.1:5000/questions/search -X POST  -H"Content-Type: application/json" -d"{'searchTerm':"what"}"`
`/categories/<int:category_id>/questions`|GET| Retrive all the questions as a List for a given category|`{'success': <Bool>, 'questions': [<obj>], 'category_name': <String>}`|`curl http://127.0.0.1:5000/categories/2/questions`
`/quizzes`|POST| Retrive a question from a given category that is didn't answered yet.|`{'success': <Bool>, 'question': <obj>}`|`curl http://127.0.0.1:5000/quizzes -X POST -H"Content-Type: application/json" -d"{'previous_questions':[<obj>], 'quiz_category': <int>}"`

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```