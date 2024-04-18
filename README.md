# CodeAmici

## Tech Stack

## Prerequisites

Here is what you need to be able to run CodeAmici

- Docker

## Environment Setup

1. Clone the repository

   ```sh
   https://github.com/ShyamGadde/code-amici.git
   ```

2. Go to the project folder

   ```sh
   cd code-amici
   ```

3. Configure your `.env` file

   - Make a copy of `.env.example` and rename it to `.env`
   - The keys under `# Database` are pre-configured for the Docker setup and should not be changed
   - The keys under `# JWT` can be modified as per your requirements
   - To generate a new secret key use `openssl rand -hex 32` and replace the `SECRET_KEY` value in the `.env` file

4. Run Docker Compose

   ```sh
   docker-compose build --no-cache
   docker-compose up -d
   ```

5. Populate database with dummy user data

   ```sh
   docker-compose exec backend python utils/seed_db.py
   ```

6. Stopping the Application

   To stop the application and remove the containers, networks, and volumes defined in your docker-compose.yml file, run the following command:

   ```sh
   docker
   ```

## How to use

1. Open up a web browser and head over to http://localhost:5000/.

## How it works

### Recommendation System

### Backend API

### Authentication

## Acknowledgements
