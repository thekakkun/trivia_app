# Trivia App

A project for [Udacity"s Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044), Part 2: API Development and Documentation.

Check out the [original repo](https://github.com/udacity/cd0037-API-Development-and-Documentation-project) for more information on the project, or [see the rest of the projects completed for the nanodegree](https://github.com/thekakkun/udacity_projects).

## Tech Stack (Dependencies)

### Backend Dependencies

- Flask
- SQLAlchemy

### Frontent Dependencies

- React

## API Documentation

### Getting started

- The app is run locally, and is not hosted as a base URL. The backend is hosted at the default `http:127.0.0.1:5000/`.
- No authentication or API keys are required

### Error Handling

Errors are returned in the following format:

```json
{
  "code": 404,
  "description": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
  "name": "Not Found"
}
```

The following types of errors are returned, depending on the request:

- 404: Not found
- 405: Method not allowed
- 422: Unprocesseable request

### Endpoints

#### `GET /categories`

Get a list of the categories questions can belong in.

##### Sample

- Request: `curl -X GET http:127.0.0.1:5000/categories`
- Response:
  ```json
  {
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    }
  }
  ```

#### `GET /questions?page={integer}`

Get a list of questions.

##### Query strings

- `page` (integer, optional): Questions are split into pages of 10. Set a value to return the specified page, or the first page if left out.

##### Sample

- Request: `curl -X GET http:127.0.0.1:5000/questions?page=1`
- Response:
  ```json
  {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    ...
  ],
  "total_questions": 19
  }
  ```

#### `DELETE /questions/{question_id}`

Delete the specified question.

##### Sample

- Request: `curl -X DELETE http:127.0.0.1:5000/questions/1`
- Response: An empty json object will be returned if successful.

#### `POST /questions`

##### Request Body

###### Search

- `SearchTerm` (string, required): Term to search for. The search will be case-insensitive.

```json
{
  "searchTerm": "foo"
}
```

###### Add a new question

- `question` (string, required): The question to add
- `answer` (string, required): Answer to the question being added
- `category` (integer, required): Category the question belongs to
- `difficulty` (integer, required): Difficulty of the question

```json
{
  "question": "What is the largest mammal?",
  "answer": "Blue whale",
  "category": 1,
  "difficulty": 2
}
```

##### Query strings

- `page` (integer, optional): Questions are split into pages of 10. Set a value to return the specified page, or the first page if left out.

##### Sample

###### Search

- Request: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm":"The"}'`
- Response:
  ```json
  {
  "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
  },
  "current_category": null,
  "questions": [
      {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled "I Know Why the Caged Bird Sings"?"
      },
      ...
  ],
  "total_questions": 11
  }
  ```

###### Add a new question

- Request: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "What is the largest mammal?", "answer": "Blue whale", "category": 1, "difficulty": 2}'`
- Response:
  ```json
  {
  "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
  },
  "current_category": null,
  "questions": [
      {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled "I Know Why the Caged Bird Sings"?"
      },
      ...
  ],
  "total_questions": 11
  }
  ```

#### `GET /categories/{category_id}/questions`

Get a list of questions based on the specified category.

##### Query strings

- `page` (integer, optional): Questions are split into pages of 10. Set a value to return the specified page, or the first page if left out.

##### Sample

- Request: `curl -X GET http://127.0.0.1:5000/categories/1/questions`
- Response:
  ```json
  {
  "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
  },
  "current_category": "Science",
  "questions": [
      {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
      },
      ...
  ],
  "total_questions": 3
  }
  ```

#### `POST /quizzes`

Play the quiz. Returns a single random question belonging to the category.

##### Request body

- `quiz_category` (string, required): The category to pull questions from.
- `previous_questions` (list of int, required): IDs to remove from pool of possible questions

```json
{
  "quiz_category": { "id": "2", "type": "Art" },
  "previous_questions": [16, 17, 18]
}
```

##### Sample

- Request: `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category": {"id": "2", "type": "Art"}, "previous_questions": [16, 17, 18]}'`
- Response:
  ```json
  {
    "question": {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  }
  ```
