import os
from dotenv import load_dotenv
from agents import LearningAssistant

load_dotenv(override=True)
together_api_key = os.getenv("TOGETHER_API_KEY")


if __name__ == "__main__":
    assistant = LearningAssistant()
    assistant.fetch_qa_from_image()