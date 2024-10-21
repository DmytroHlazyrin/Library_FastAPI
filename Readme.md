# Library Management API

This project is a **Library Management API** built using **FastAPI**, **SQLAlchemy**, and **SQLite**. It allows managing authors, books, publishers, genres, users, and borrowing history. The API also supports user authentication with admin roles.

## Features

- **Authors**: Create, read, update, and delete author information.
- **Books**: Manage books, including the ability to borrow and return books.
- **Genres**: Add and list genres for books.
- **Publishers**: Manage publishers and their books.
- **Users**: Handle user registration and authentication. Admin users can perform advanced operations.
- **Borrowing History**: Track the borrowing and returning history of books.
- **Pagination and Sorting**: Use query parameters for sorting and paginating responses.

## Getting Started

### Prerequisites

- Python 3.10+
- FastAPI
- SQLAlchemy
- Uvicorn (for running the FastAPI app)

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/DmytroHlazyrin/Library_FastAPI.git
    cd Library_FastAPI
    ```

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv env
    source env/bin/activate  # For Linux/macOS
    env\Scripts\activate  # For Windows
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

### Running the API

1. **Apply migrations** (if needed):

    For this project, migrations are managed manually by defining the models and creating the database schema. You can create the database file by running the server for the first time or manually.

2. **Run the FastAPI server**:

    ```bash
    uvicorn app.main:app --reload
    ```

    The app will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

3. **Explore the API**:

    Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to interact with the API using the automatically generated Swagger UI.

### API Endpoints

Here are some of the key endpoints for this API:

- **/authors**: Manage authors (requires admin role for creation).
- **/books**: Manage books and borrowing operations.
- **/genres**: List and create genres.
- **/publishers**: Manage publishers.
- **/users**: User registration and authentication.
- **/login**: User authentication to get JWT token.
- **/me/debts**: Get active borrowings for the authenticated user.

For a complete list of endpoints and to test them, refer to the [API documentation](http://127.0.0.1:8000/docs).

### Environment Variables

- `DATABASE_URL`: Set the database connection string (SQLite in this case).
- `SECRET_KEY`: Secret key for hashing password.
- `ALGORITHM`: Hashing algorithm.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expire time in minutes.

### Running Tests

Tests are written using **pytest** and cover all key functionality, including borrowing operations, user management, and access control.

To run tests, execute:

```bash
pytest
```

This will automatically run all the tests in the tests directory.

### Fixtures
Several fixtures are used to provide test data. Here are some key fixtures:

* admin_user: An admin user with elevated privileges.
* user: A regular user with borrowing rights.
* create_authors: A sample authors for testing.
* create_publishers: A sample publishers for testing.
* create_genres: A sample genres for testing.
* create_books: Creates a books with an associated author, publisher, and genre.

### Database
The project uses SQLite as the database engine for simplicity. 
You can change this to another database by updating the DATABASE_URL environment variable in env.py

### Authentication
The API uses JWT for authentication and role-based access control. Normal users and admin users have different permissions.

#### Normal users: 
Can borrow and return books, 
read authors, books, genres, publishers, and view own borrowing history and debts.

#### Admin users: 
Can manage authors, books, genres, publishers, and view borrowing history, debtors.

### License
This project is licensed under the MIT License.