# 247digitalhub

247digitalhub is a modern web application built with Django 5 and MySQL, designed to provide seamless digital services. The project is containerized using Docker, but it can also be run locally without Docker. Authentication is handled using `django-allauth`, providing flexible and secure user authentication.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [Without Docker](#without-docker)
  - [With Docker](#with-docker)
- [Running the Project](#running-the-project)
  - [Without Docker](#without-docker)
  - [With Docker](#with-docker)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.10
- Django 5
- MySQL
- Docker (optional, for containerized setup)
- Docker Compose (optional, for containerized setup)

## Installation

### Without Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ChidiebereIbiam/digitalhub.git
   cd digitalhub
   ```

2. **Create a virtual environment:**

   ```bash
   python3.10 -m venv env
   source env/bin/activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   Ensure MySQL is installed and running. Create a database and a user with the necessary privileges:

   ```sql
   CREATE DATABASE digitalhub_db;
   CREATE USER 'yourusername'@'localhost' IDENTIFIED BY 'yourpassword';
   GRANT ALL PRIVILEGES ON 247digitalhub_db.* TO 'yourusername'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Configure environment variables:**

   Create a `.env` file in the project root and add the following:

   ```bash
   DEBUG=True
   SECRET_KEY=your_secret_key
   MYSQL_DATABASE=247digitalhub_db
   MYSQL_USER=yourusername
   MYSQL_PASSWORD=yourpassword
   HOST=localhost
   PORT=3306
   ```

6. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

### With Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ChidiebereIbiam/digitalhub.git
   cd digitalhub
   ```

2. **Build and start the Docker containers:**

   ```bash
   docker-compose up --build
   ```

3. **Create a superuser:**

   After the containers are up and running, you can create a superuser by executing the following command inside the web container:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Running the Project

### Without Docker

1. **Activate the virtual environment:**

   ```bash
   source env/bin/activate
   ```

2. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

   The project will be accessible at `http://127.0.0.1:8000/`.

### With Docker

1. **Start the Docker containers:**

   ```bash
   docker-compose up
   ```

   The project will be accessible at `http://127.0.0.1:8000/`.

## Environment Variables

Ensure you have the following environment variables set in your `.env` file:

- `DEBUG`: Set to `True` for development, `False` for production.
- `SECRET_KEY`: A secret key for your Django application.
- `MYSQL_DATABASE`: Name of your MySQL database.
- `MYSQL_USER`: MySQL database username.
- `MYSQL_PASSWORD`: MySQL database password.
- `HOST`: Database host, typically `localhost` or the name of your MySQL container in Docker.
- `PORT`: Port on which MySQL is running, typically `3306`.

## Database Migrations

To apply database migrations, use the following command:

- **Without Docker:**

  ```bash
  python manage.py migrate
  ```

- **With Docker:**

  ```bash
  docker-compose exec web python manage.py migrate
  ```

## Usage

- **Admin Panel:** Access the Django admin panel at `http://127.0.0.1:8000/admin/` using the superuser credentials.
- **Authentication:** `django-allauth` is configured to manage user authentication. You can extend or customize the authentication views as needed.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

