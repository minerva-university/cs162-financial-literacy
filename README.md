# Financial Literacy Marketplace

## Project Overview
The Financial Literacy Marketplace is a comprehensive web application designed to provide college students with essential financial resources. The platform enables users to:

- Find and connect with mentors.
- Explore scholarships and internships.
- Post and engage with content related to financial literacy, including topics like loans, credit cards, and more.

This project aims to enhance financial awareness among students by offering a centralized hub for knowledge and mentorship opportunities.

---

## Features

### How the App Works

1. **User Authentication**:
   - Users can sign up and log in to create personalized accounts.
   - Profiles are securely managed, allowing users to access their activities and contributions.

2. **Mentorship System**:
   - Users can browse mentor profiles based on expertise, company, or university.
   - Sessions can be requested, with integration to scheduling tools like Google Calendar (and more in development).
   - Mentors earn credits for sessions, while mentees use credits to book them.

3. **Scholarships and Internships**:
   - A searchable database allows users to explore opportunities filtered by deadline, type, or organization.
   - Users can add or manage listings, ensuring up-to-date opportunities are available to the community.

4. **Posts and Engagement**:
   - Users can create posts on financial topics or share resources.
   - Posts support upvotes, downvotes, and comments to encourage discussions.
   - Moderation features include AI-based initial review and community approval workflows (planned).

5. **Gamified Credit System**:
   - Credits incentivize participation. Users start with a base amount and earn more by posting or mentoring.
   - Credits are deducted for accessing resources or mentorship sessions, promoting active contribution to the platform.

---

## Installation

### Prerequisites
- **Node.js**: Required for running the frontend.
- **Python 3.x**: Required for backend operations.
- **Database**: Online database configured (SQLite and others supported).

### Backend Setup Instructions

1. **Clone the repository**:
   ```sh
   git clone https://github.com/minerva-university/cs162-financial-literacy.git
   cd cs162-financial-literacy/backend
   ```

2. **Create and activate a virtual environment (optional but recommended)**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the `.env` file**:
   Create a `.env` file in the `backend` directory and add the following environment variables:

   ```env
   FLASK_APP=wsgi.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   db_uri=your_database_url
   ```

   Replace `your_secret_key` with a secret key of your choice and `your_database_url` with the URL of your database.

5. **Run the Flask application**:
   ```sh
   flask run
   ```

6. **Access the application**:
   Open your web browser and navigate to `http://127.0.0.1:5000/` to access the application.

### Frontend Setup Instructions

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend server:
   ```bash
   npm start
   ```

---

## Project Structure

```plaintext
cs162-financial-literacy/
├── .github/
│   └── workflows/
│       ├── cd.yml               # Continuous Deployment workflow
│       └── ci.yml               # Continuous Integration workflow
├── backend/
│   ├── database/                # Database initialization and sample data
│   │   ├── add_sample_scholarship.py
│   │   ├── add_sample_user.py
│   │   ├── create.py
│   │   ├── create.sql
│   │   ├── cs162_financial_literacy.db
│   │   └── path_to_your_database.db
│   ├── secrets/                 # Secret keys (if applicable)
│   ├── unittest/                # Unit tests
│   ├── venv/                    # Virtual environment
│   ├── __init__.py              # Backend initialization
│   ├── .env                     # Environment variables
│   ├── .gitignore               # Git ignore file
│   ├── auth.py                  # Authentication logic
│   ├── config.py                # Backend configuration
│   ├── google_calendar.py       # Google Calendar integration
│   ├── mentorship.py            # Mentorship routes
│   ├── posts.py                 # Post management routes
│   ├── profile.py               # Profile management
│   ├── requirements.txt         # Dependencies
│   ├── scholarships_internships.py # Scholarships and internships routes
│   ├── wsgi.py                  # WSGI entry point
│   ├── README_credit.md         # Backend-specific credits
│   └── README.md                # Backend documentation
├── frontend/
│   ├── public/                  # Public assets
│   │   ├── images/
│   │   ├── favicon.png
│   │   └── index.html
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   │   ├── CalendarView.js
│   │   │   ├── Feed.js
│   │   │   ├── Footer.js
│   │   │   ├── Navbar.js
│   │   │   └── Post.js
│   │   ├── pages/               # Page-specific components
│   │   │   ├── AboutUsPage.js
│   │   │   ├── Login.js
│   │   │   ├── ScholarshipsPage.js
│   │   │   └── UserProfile.js
│   │   ├── services/            # API integrations
│   │   │   └── api.js
│   │   ├── styles/              # CSS files
│   │   │   ├── App.css
│   │   │   ├── Navbar.css
│   │   │   ├── PostFeed.css
│   │   │   └── ProfilePage.css
│   │   ├── App.js               # Main React component
│   │   ├── index.js             # React entry point
│   │   └── index.css            # Global styles
│   ├── .env                     # Environment variables
│   ├── package.json             # Project dependencies
│   ├── package-lock.json        # Lock file for dependencies
│   ├── tailwind.config.js       # Tailwind CSS configuration
│   ├── Dockerfile               # Docker configuration
│   ├── .gitignore               # Git ignore file
│   ├── .dockerignore            # Docker ignore file
│   ├── README.md                # Frontend documentation
│   └── .coverage                # Test coverage
└── README.md                    # Main project documentation
```

---

## Contribution Guide

### Git Workflow

1. Clone the repository and create a new branch for your feature:
   ```bash
   git checkout -b feature-branch
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "Feature description"
   ```

3. Push changes and create a pull request:
   ```bash
   git push origin feature-branch
   ```

### Branch Naming Conventions

- **`main`**: Stable production-ready code.
- **`signup-front-backend`**: Integration of frontend and backend for user signup.
- **`mentorship`**: Features related to mentorship functionality.
- **`scholarships-internships-frontend`**: Frontend for managing scholarships and internships.

---

## Development Progress

### Current Status

- Backend is functional with basic features implemented.
- Frontend has partially implemented mentorship, scholarships, and internship features.
- Sample data is being used for testing and demonstration.

### Known Issues

- Post rendering delays.
- Profile management has incomplete features (e.g., profile picture upload).
- Limited calendar integrations.

---

## Future Plans

- **Enhanced UI/UX**:
  - Intuitive navigation.
  - Improved responsiveness.
- **AI Integration**:
  - Post verification using AI.
  - Personalized recommendations.
- **Expanded Calendar Support**:
  - Integrations with Apple Calendar and other services.
- **Moderation Tools**:
  - Role-based access for moderators.

---

## Acknowledgements

This project is the result of collaborative efforts by the CS162 development team. Special thanks to contributors who have made significant advancements in both frontend and backend development.

---
