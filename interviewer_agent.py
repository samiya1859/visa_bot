from typing import List, Dict
from dataclasses import dataclass
import json
from enum import Enum
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process,LLM

QUESTIONS_FILE = "questions.json"

class VisaType(str, Enum):
    B1_B2 = "B1/B2"
    F1 = "F1"
    H1B = "H1B"
    MEDICAL = "Medical"

@dataclass
class InterviewSession:
    visa_type: VisaType
    country: str
    answers: List[Dict] = None

    def __post_init__(self):
        self.answers = [] 

class MockInterviewAgent:
    def __init__(self, api_key: str):
        self.llm = LLM(
            model="gpt-4",
            api_key=api_key
        )
        self.questions = self.load_questions()

    def load_questions(self):
        with open(QUESTIONS_FILE, 'r') as f:
            return json.load(f)

    def create_agents(self):
        agents = {
            'question_collector': Agent(
                role='Question Collector',
                goal='Select appropriate questions based on visa type and country',
                backstory="I analyze visa requirements and select relevant questions for each category.As you are an expert interviewer you can generate new questions basis on the provided questions.",
                llm=self.llm
            ),
            'interviewer': Agent(
                role='Visa Officer',
                goal='Conduct structured interview following category order',
                backstory="I conduct interviews professionally, following a logical sequence.And give comfort and make relax the applicant",
                llm=self.llm
            ),
            'editor': Agent(
                role='Answer Improver',
                goal='Enhance answers while maintaining authenticity',
                backstory="I help improve answers to better convey the applicant's intent.",
                llm=self.llm
            ),
            'evaluator': Agent(
                role='Performance Assessor',
                goal='Evaluate overall interview performance',
                backstory="I provide comprehensive feedback on interview responses.",
                llm=self.llm
            ),
            'final_assessor': Agent(
                role='Final Assessor',
                goal='Provide comprehensive evaluation',
                backstory="Expert in final visa interview assessments.",
                llm=self.llm
            )
        }
        return agents

    def create_tasks(self, agents: dict, interview_session: InterviewSession) -> List[Task]:
        return [
            Task(
                description=f"Collect questions for {interview_session.visa_type.value} visa interview for {interview_session.country}.",
                agent=agents['question_collector'],
                expected_output="A list of relevant interview questions organized by category"
            ),
            Task(
                description="Conduct interview with collected questions.",
                agent=agents['interviewer'],
                expected_output="A dictionary containing questions and answers from the interview"
            ),
            Task(
                description="Evaluate answers with scores and feedback.",
                agent=agents['evaluator'],
                expected_output="A dictionary containing scores and feedback for each answer"
            ),
            Task(
                description="Improve answers while maintaining authenticity.",
                agent=agents['editor'],
                expected_output="A dictionary containing improved versions of each answer"
            ),
            Task(
                description="Provide comprehensive interview assessment.",
                agent=agents['final_assessor'],
                expected_output="A detailed assessment report with recommendations"
            )
        ]

    def create_crew(self, interview_session: InterviewSession):
        agents = self.create_agents()
        tasks = self.create_tasks(agents, interview_session)
        
        return Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )

    def run_interview(self, interview_session: InterviewSession):
        crew = self.create_crew(interview_session)
        return crew.kickoff()

def main():
    try:
        print("AI-Powered Visa Interview Practice System")
        
        country = input("\nCountry applying to: ").strip()
        print("\nVisa types:")
        for i, visa_type in enumerate(VisaType, 1):
            print(f"{i}. {visa_type.value}")

        while True:
            try:
                visa_choice = int(input("Select visa type (1-4): "))
                if 1 <= visa_choice <= len(VisaType):
                    break
                print("Invalid choice. Please select 1-4.")
            except ValueError:
                print("Please enter a valid number.")

        visa_type = list(VisaType)[visa_choice - 1]
        session = InterviewSession(visa_type=visa_type, country=country)
        
        # Load API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("Error: OPENAI_API_KEY is not set in the environment variables.")
            return
        
        agent = MockInterviewAgent(api_key=api_key)
        result = agent.run_interview(session)
        
        print("\nInterview Results:")
        print(result)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()