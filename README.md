# AI-Powered Visa Processing Agent

## visa agent
This project allows users to interact with an AI agent that searches government embassy websites to extract necessary visa document requirements. The backend is built using Django and Django REST Framework (DRF), and the AI agent extracts and provides detailed information based on the requested visa type and country.

## Requirements
The project requires Python 3.8 or higher, along with Django and Django REST Framework. The core functionality is powered by an AI agent that interacts with government embassy websites to extract visa document information.


## Setup and Installation

### 1. Clone the repository

Clone the project repository and navigate to the `visa_agent` directory.

```bash
git clone https://github.com/samiya1859/visa_bot.git
cd visa_bot
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

### 5. API Endpoints
 (POST)](http://127.0.0.1:8000/api/visa-search/)
This endpoint accepts a POST request with the visa type and country, and the AI agent will retrieve the necessary visa document requirements.

Request Body (JSON):
```json
{
    "country": "Thiland",
    "visa_type": "Tourist"
}

Response (JSON):
"id": 1,
        "country": "Thiland",
        "visa_type": "Tourist",
        "embassy_url": "https://dhaka.thaiembassy.org/en/publicservice/tourist-visa-tr?page=5d83296315e39c2540006a6c&menu=5d83296315e39c2540006a6d",
        "visa_information": "For obtaining a Royal Thai Tourist Visa, applicants must carefully prepare and submit the required documentation. Below is a clear and organized presentation of the necessary documents and important instructions:\n\n1. **Required Documents:**\n   - **Completed Visa Application Form:** Fill out the form accurately with all required details.\n   - **Passport:** Ensure your passport is valid for at least six ..........
        "status": "success",
        "created_at": "2025-01-22T07:54:50.927530Z"
```

### 6.How It Works
Backend - Visa Manager (visa_manager.py)
The core functionality of visa document extraction is implemented in the visa_manager.py file inside the chatbot app.

#### AI Agent:

The AI agent interacts with OpenAI’s GPT-4 model to search for necessary visa documents from official embassy websites.
The agent uses the provided visa type and country to find the corresponding embassy website and extract the required documents.
#### Django REST Framework (DRF):

The API is built using Django REST Framework to handle incoming requests and responses in a structured manner.
Users can submit a visa type and country via a POST request, and the AI agent will return a list of required documents.


## Front end UI 
Here you will be able to experience an attractive UI developed by HTML,CSS,JS,Bootstrap.
how you will run this : 
after cloning the repository do : 
```bash
cd visa_bot
cd HACKATHON TravelDesk AI
```
then open index.html and run that file with liver server


## Mock Interviewer Agent
Here a mock interview crew is introduced.

#### Functionalities :
- One agent gather all relevant questions generally asked by a visa officer
- interviewer agent asks questions one by one.
- an editor agent re writes better answers tailoring visa types and country.
- an evolution agent gives a feedback according to the interview.

#### run the script file :
cloning the repository 
```bash
cd visa_bot
```
export your api key in your bash 
```bash
export OPENAI_API_KEY="your api key"
```
then
```bash
python interviewer_agent.py
```


