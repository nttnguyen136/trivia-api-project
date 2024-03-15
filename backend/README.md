# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```




## ENDPOINTS

`GET '/categories'`
* Fetches a dictionary of categories
* Request Arguments: None
* Returns:
  * `success`: A boolean indicating the success of the request.
  * `categories`: An object of categories
```json
  {
    'categories': { 
      {'id': 1, 'type':'Science'},
      {'id': 2, 'type':'Art'},
      {'id': 3, 'type':'Geography'},
      {'id': 4, 'type':'History'},
      {'id': 5, 'type':'Entertainment'}
      {'id': 6, 'type':'Sports'},
    }
  }
```

`GET '/questions?page=${integer}'`
* Fetches a paginated set of questions, a total number of questions, all categories and current category string.
* Request Arguments: `page` - integer
* Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
```json
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History',
    'categories': {
      {'id': 1, 'type':'Science'},
      {'id': 2, 'type':'Art'},
      {'id': 3, 'type':'Geography'},
      {'id': 4, 'type':'History'},
      {'id': 5, 'type':'Entertainment'},
      {'id': 6, 'type':'Sports'},
    },
}

```


`GET '/categories/${id}/questions'`
* Fetches questions for a cateogry specified by id request argument
* Request Arguments: `id` - integer
* Returns: An object with questions for the specified category, total questions, and current category string
```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 4
        },
    ],
    "totalQuestions": 100,
    "currentCategory": "History"
}
```


`DELETE '/questions/${id}'`
* Deletes a specified question using the id of the question
* Request Arguments: `id` - integer
* Returns: Success message
```json
{
    "success": true,
    "message": "Question deleted successfully"
}
```


`POST '/quizzes'`
* Sends a post request in order to get the next question
* Request Body:
```json
{
    "previous_questions": [1, 4, 20, 15],
    "quiz_category": "current category"
 }
```
* Returns: a single new question object
```json
{
    "question": {
        "id": 1,
        "question": "This is a question",
        "answer": "This is an answer",
        "difficulty": 5,
        "category": 4
    }
}
```


`POST '/questions'`
* Sends a post request in order to add a new question
* Request Body:
```json
{
    "question":  "Heres a new question string",
    "answer":  "Heres a new answer string",
    "difficulty": 1,
    "category": 3,
}
```
* Returns: Return success status and new questions ID
```json
{
    "success": True,
    "message": "Question created successfully",
    "question_id": 1,
}
```


`POST '/questions/search'`
* Sends a post request in order to search for a specific question by search term
* Request Body:
```json
{
    "searchTerm": "searching"
}
```
* Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 5
        },
    ],
    "totalQuestions": 100,
    "currentCategory": "Entertainment"
}
```

