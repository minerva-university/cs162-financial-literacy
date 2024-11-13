# cs162-financial-literacy

## To run the backend

### Prerequisites

- Python 3.x
- pip (Python package installer)
- virtualenv (optional but recommended)

### Setup Instructions

1. **Clone the repository:**

   ```sh
   git clone https://github.com/minerva-university/cs162-financial-literacy.git
   cd cs162-financial-literacy/backend
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the `.env` file:**

   Create a `.env` file in the `backend` directory and add the following environment variables:

   ```env
   FLASK_APP=wsgi.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   ```

   Replace `your_secret_key` with a secret key of your choice and `your_database_url` with the URL of your database.

5. **Run the Flask application:**

   ```sh
   flask run
   ```

### Additional Information

- **Access the application:**
  Open your web browser and navigate to `http://127.0.0.1:5000/` to access the application.

- **Deactivate the virtual environment:**
  When you are done working on the project, you can deactivate the virtual environment by running:

  ```sh
  deactivate
  ```

### Troubleshooting

- If you encounter any issues, ensure that all dependencies are installed correctly and that the `.env` file is set up properly.
- Check the terminal output for any error messages and address them accordingly.
