# AI-Powered Visa Processing Agent

## visa agent
This project allows users to interact with an AI agent that searches government embassy websites to extract necessary visa document requirements. The backend is built using Django and Django REST Framework (DRF), and the AI agent extracts and provides detailed information based on the requested visa type and country.

## Requirements
The project requires Python 3.8 or higher, along with Django and Django REST Framework. The core functionality is powered by an AI agent that interacts with government embassy websites to extract visa document information.
---

## Setup and Installation

### 1. Clone the repository

Clone the project repository and navigate to the `visa_agent` directory.

```bash
git clone https://github.com/samiya1859/visa_agent.git
cd visa_agent
```
### 2. Set up the Backend
Install dependencies:
```bash
pip install -r requirements.txt
```
### 3. Set up environment variables:
Create a .env file in the visa_agent/ directory and add the following content for your API keys and sensitive information:

```plaintext
OPENAI_API_KEY=your-api-key-here
GOOGLE_API_KEY=your-google-api-key-here
```
Make sure to replace the placeholders with your actual API keys.

### 4. Migrate the database:
Run the following command to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Run the server:
Start the Django development server:

```bash
python manage.py runserver
```
The server will be available locally at http://127.0.0.1:8000/.
