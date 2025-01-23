import openai
import json
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from crewai import Agent, Task, Crew, LLM
from googlesearch import search
import logging
import re

load_dotenv()

class VisaManager:
    def __init__(self, country, visa_type):
        self.country = country
        self.visa_type = visa_type
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Keywords to identify document-related information
        self.doc_keywords = [
            'visa requirements', 'required documents', 'documentation',
            'visa application', 'supporting documents', 'checklist',
            f'{visa_type} visa', 'application process'
        ]
        
        self.llm = LLM(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def search_embassy_website(self):
        """Search for the official embassy website using Google"""
        try:
            query = f"{self.country} embassy {self.visa_type} visa official website"
            search_results = list(search(query, num_results=3))
            
            # Filter for official domains
            official_sites = [url for url in search_results if self._is_official_domain(url)]
            return official_sites[0] if official_sites else search_results[0]
        except Exception as e:
            self.logger.error(f"Error searching embassy website: {str(e)}")
            return None

    def _is_official_domain(self, url):
        """Check if URL is an official government domain"""
        govt_domains = ['.gov', '.gob', '.gouv', '.gov.uk', '.gc.ca', 
                       'embassy', 'consulate', 'diplomatic']
        return any(domain in url.lower() for domain in govt_domains)

    def get_embassy_website_content(self, url):
        """Get and parse embassy website content"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unnecessary elements
            for element in soup(['script', 'style', 'footer', 'nav']):
                element.decompose()
                
            return soup
        except Exception as e:
            self.logger.error(f"Error getting website content: {str(e)}")
            return None

    def extract_visa_information(self, soup):
        """Extract relevant visa information from the webpage"""
        if not soup:
            return "Could not extract website content"

        relevant_content = []
        
        # Look for relevant sections
        for keyword in self.doc_keywords:
            elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li'], 
                                  string=re.compile(keyword, re.IGNORECASE))
            
            for element in elements:
                # Get the containing section
                section = element.find_parent(['div', 'section']) or element
                text = self._clean_text(section.get_text())
                if text and len(text) > 20:  # Avoid very short snippets
                    relevant_content.append(text)

        return '\n'.join(relevant_content)

    def _clean_text(self, text):
        """Clean and normalize text content"""
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s.,()-]', '', text)
        return text

    def create_agents(self):
        researcher = Agent(
            role='Embassy Website Researcher',
            goal=f'Find and analyze embassy website for {self.country} {self.visa_type} visa requirements',
            backstory="""Expert in finding and analyzing official embassy websites and visa information. 
                        Capable of distinguishing official sources and extracting relevant visa requirements.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        document_agent = Agent(
            role='Visa Document Analyzer',
            goal=f'Extract and verify document requirements for {self.visa_type} visa',
            backstory="""Specialized in analyzing visa documentation requirements and ensuring 
                        all necessary documents are identified and properly listed.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        user_agent = Agent(
            role='Information Presenter',
            goal='Present visa information clearly to the user',
            backstory="""Expert in organizing and presenting visa information in a clear, 
                        user-friendly format with emphasis on required documentation.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        return researcher, document_agent, user_agent

    def create_tasks(self, researcher, document_agent, user_agent):
        research_task = Task(
            description=f"""Research {self.country} embassy website for {self.visa_type} visa:
                          1. Find official embassy website
                          2. Extract relevant visa information
                          3. Identify document requirements section""",
            agent=researcher,
            expected_output="A detailed report of the embassy website findings and visa information."
        )

        document_task = Task(
            description=f"""Analyze the visa requirements:
                          1. Extract all required documents
                          2. Identify special requirements or formats
                          3. Note any additional documentation needs""",
            agent=document_agent,
            expected_output="A comprehensive list of required documents and special requirements."
        )

        presentation_task = Task(
            description="""Present the information to the user:
                          1. List all required documents clearly
                          2. Include any special instructions
                          3. Add important notes or warnings""",
            agent=user_agent,
            expected_output="A clear, organized presentation of visa requirements and documents."
        )

        return [research_task, document_task, presentation_task]

    def run(self):
        try:
            # Find embassy website
            embassy_url = self.search_embassy_website()
            if not embassy_url:
                return {"error": "Could not find embassy website"}

            # Get website content
            soup = self.get_embassy_website_content(embassy_url)
            if not soup:
                return {"error": "Could not access embassy website"}

            # Extract visa information
            visa_info = self.extract_visa_information(soup)

            # Create and run the agent crew
            researcher, document_agent, user_agent = self.create_agents()
            tasks = self.create_tasks(researcher, document_agent, user_agent)

            crew = Crew(
                agents=[researcher, document_agent, user_agent],
                tasks=tasks,
                verbose=True
            )

            # Process the information using the crew
            result = crew.kickoff()

            return {
                "status": "success",
                "embassy_url": embassy_url,
                "visa_information": result
            }

        except Exception as e:
            self.logger.error(f"Error in visa manager: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    print("\n=== Welcome to Visa Information Assistant ===")
    print("This tool will help you find visa requirements for different countries.")
    
    while True:
        try:
            print("\nPlease enter the following information:")
            print("(Type 'exit' at any prompt to quit)")
            
            # Get country input
            country = input("\nEnter country name: ").strip()
            if country.lower() == 'exit':
                break
                
            # Get visa type input
            print("\nCommon visa types: Tourist, Business, Student, Work, Transit")
            visa_type = input("Enter visa type: ").strip()
            if visa_type.lower() == 'exit':
                break
            
            # Create visa manager instance
            print(f"\nSearching visa information for {country} - {visa_type} visa...")
            visa_manager = VisaManager(country=country, visa_type=visa_type)
            
            # Get results
            result = visa_manager.run()
            
            # Display results
            if result.get("status") == "success":
                print("\n" + "="*50)
                print(f"Visa Information for {country} ({visa_type} visa)")
                print("="*50)
                print(f"\nSource: {result['embassy_url']}")
                print("\nDocument Requirements and Information:")
                print("-"*50)
                print(result['visa_information'])
                print("\n" + "="*50)
            else:
                print(f"\nError: {result.get('message', 'An unknown error occurred')}")
            
            # Ask if user wants to continue
            continue_search = input("\nWould you like to search for another visa? (yes/no): ").strip().lower()
            if continue_search != 'yes':
                break
                
        except KeyboardInterrupt:
            print("\n\nExiting program...")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")
            
    print("\nThank you for using Visa Information Assistant!")

if __name__ == "__main__":
    main()