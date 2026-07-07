# Architecture Overview

## 1. High-Level Architecture
The Audio-Speech-To-Sign-Language-Converter is a web-based application built on the Django framework. The primary goal of the system is to take live audio speech input from a user, process the speech into text using web speech APIs, analyze the text using Natural Language Processing (NLP), and output a sequence of corresponding Indian Sign Language (ISL) animations.

### System Flow
1. **Input Generation**: The user accesses the web interface and interacts with the application. By utilizing the browser's `webkitSpeechRecognition` API, the user records their speech which is converted directly into text on the client-side.
2. **Request Handling**: The text data is submitted via a POST request to the Django backend.
3. **Natural Language Processing (NLP)**: The backend processes the string using NLTK (Natural Language Toolkit). 
   - Tokenization: Splitting sentences into words.
   - Part-of-Speech (POS) Tagging: Identifying verbs, nouns, adjectives, etc.
   - Lemmatization: Reducing words to their base or dictionary form (e.g., "running" becomes "run").
   - Stop-word Removal: Filtering out common words that lack significant meaning in sign language.
4. **Tense Resolution**: Rules are applied to adapt sentence structure for sign language (e.g., appending "Now" for present continuous or "Before" for past tense).
5. **Animation Mapping**: The processed words are mapped to pre-rendered `.mp4` video animations in the `assets/` directory. If an exact word match doesn't exist, the system falls back to spelling out the word letter-by-letter.
6. **Output Rendering**: The server responds with an HTML page embedding a sequence of the chosen animations, which the frontend's JavaScript automatically plays in order.

## 2. Directory Structure & Components
- **`A2SL/`**: The core Django project directory containing:
  - `settings.py`: Central configuration file managing installed apps, middleware, databases, and static paths.
  - `urls.py`: Defines the routing for the application, mapping URLs to view functions.
  - `views.py`: Contains the main business logic including user authentication and the NLP processing for the `animation_view`.
- **`templates/`**: Holds all the HTML templates for the frontend (e.g., `base.html`, `animation.html`, `home.html`). Uses Django Template Language for dynamic rendering.
- **`assets/`**: The static file directory holding CSS, images, and the `.mp4` sign language video files.
- **`db.sqlite3`**: The local SQLite database used primarily for Django's built-in User Authentication (signup, login).
- **`manage.py`**: The command-line utility for interacting with the Django project.

## 3. Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript.
- **Speech API**: Web Speech API (`webkitSpeechRecognition`).
- **Backend Framework**: Django (Python).
- **NLP Library**: NLTK (Natural Language Toolkit) with wordnet and averaged_perceptron_tagger.
- **Database**: SQLite3 (for User Auth).
