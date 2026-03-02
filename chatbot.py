import os
from groq import Groq
from dotenv import load_dotenv
from prompts import tech_question_prompt, system_prompt, closing_prompt
from data_handler import save_candidate_data

load_dotenv()


class HiringAssistant:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("MODEL_NAME")

        self.fields = [
            "full_name",
            "email",
            "phone",
            "experience",
            "position",
            "location",
            "tech_stack",
        ]

        self.questions = {
            "full_name": "Please provide your Full Name.",
            "email": "Please provide your Email Address.",
            "phone": "Please provide your Phone Number.",
            "experience": "How many years of experience do you have?",
            "position": "What position are you applying for?",
            "location": "What is your current location?",
            "tech_stack": "Please list your Tech Stack (languages, frameworks, tools).",
        }

        self.state = {
            "current_field_index": 0,
            "candidate_data": {},
            "tech_questions_generated": False,
        }

    def initialize_conversation(self):
        greeting = (
            "Hello 👋 Welcome to TalentScout Hiring Assistant.\n\n"
            "I'll help with your initial screening. You can type 'exit' anytime to end the conversation.\n\n"
            + self.questions[self.fields[0]]
        )
        return [{"role": "assistant", "content": greeting}]

    def handle_message(self, message, history):
        if message.lower() in ["exit", "quit", "bye"]:
            return closing_prompt()

        if not self.state["tech_questions_generated"]:
            return self.collect_field_by_field(message)

        return self.generate_followup_response(history)

    def collect_field_by_field(self, message):
        current_field = self.fields[self.state["current_field_index"]]
        self.state["candidate_data"][current_field] = message.strip()

        self.state["current_field_index"] += 1

        if self.state["current_field_index"] < len(self.fields):
            next_field = self.fields[self.state["current_field_index"]]
            return self.questions[next_field]

        save_candidate_data(self.state["candidate_data"])
        self.state["tech_questions_generated"] = True
        return self.generate_technical_questions()

    def generate_technical_questions(self):
        tech_stack = self.state["candidate_data"]["tech_stack"]
        prompt = tech_question_prompt(tech_stack)
        return self.call_llm(prompt)

    def generate_followup_response(self, history):
        prompt = system_prompt(history)
        return self.call_llm(prompt)

    def call_llm(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()