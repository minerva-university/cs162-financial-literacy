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

GitHub Copilot: To properly format the folder structure in your `README.md` file for a project that includes both a React frontend and a Flask backend, you can use Markdown code blocks. Here is an example of how you can structure it:

### Project Structure


## Project Structure

```plaintext
my_project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── index.html
│   │   └── static/
│   │       ├── css/
│   │       │   └── styles.css
│   │       └── js/
│   │           └── scripts.js
│   ├── venv/
│   ├── .env
│   ├── .gitignore
│   ├── config.py
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   └── App.js
│   │   ├── index.js
│   │   ├── App.css
│   │   └── App.test.js
│   ├── .gitignore
│   ├── package.json
│   ├── package-lock.json
│   └── README.md
└── README.md
```

### Explanation:

- `backend/`: Contains the Flask backend code.
  - `app/`: Contains the main application code.
    - `__init__.py`: Initializes the Flask app.
    - `routes.py`: Contains route definitions.
    - `models.py`: Contains database models.
    - `templates/`: Contains HTML templates.
      - `base.html`: Base template.
      - `index.html`: Home page template.
    - `static/`: Contains static files like CSS and JavaScript.
      - `css/`: Contains CSS files.
        - `styles.css`: Main stylesheet.
      - `js/`: Contains JavaScript files.
        - `scripts.js`: Main JavaScript file.
  - `venv/`: Virtual environment directory.
  - `.env`: Environment variables file.
  - `.gitignore`: Git ignore file.
  - `config.py`: Configuration file.
  - `requirements.txt`: List of dependencies.
  - `run.py`: Entry point to run the Flask app.
  - `README.md`: Backend documentation.
- `frontend/`: Contains the React frontend code.
  - `public/`: Contains public assets.
    - `index.html`: Main HTML file.
    - `favicon.ico`: Favicon file.
  - `src/`: Contains source code.
    - `components/`: Contains React components.
      - `App.js`: Main App component.
    - `index.js`: Entry point for the React app.
    - `App.css`: Main stylesheet for the React app.
    - `App.test.js`: Test file for the App component.
  - `.gitignore`: Git ignore file.
  - `package.json`: Contains project dependencies and scripts.
  - `package-lock.json`: Lock file for dependencies.
  - `README.md`: Frontend documentation.
- `README.md`: Main project documentation.
