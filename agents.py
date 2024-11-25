import sys 
import os
import json
import re
import time
import base64
import pdb
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from together import Together
from dotenv import load_dotenv
from Prompts.System import SYSTEM_CONTEXT_TEACHER, SYSTEM_CONTEXT_ANALYST
from Prompts.User import DEFAULT_USER_PROMPT, VERB_PROMPT, FETCH_PARAGRAPH, FETCH_QUESTIONS, FETCH_ANSWERS, ANALYZE_QA

load_dotenv(override=True)
together_api_key = os.getenv("TOGETHER_API_KEY")
client = Together(base_url="https://api.aimlapi.com/v1", api_key=together_api_key)

filename = sys.argv[0]
root = os.path.dirname(__file__)

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
nltk.download("averaged_perceptron_tagger_eng")



class LearningAssistant:
  def __init__(self, model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo", system_context=SYSTEM_CONTEXT_ANALYST):
    self.model = model
    self.system_context = system_context 
    self.default_prompt = DEFAULT_USER_PROMPT


  def preprocess(self, model_res):
    print("Start to pre-process")

    output = ""
    if hasattr(model_res, "choices"):
      output = model_res.choices[0].message.content
      output = output.lower()

    file_content = re.sub(r"[^\w\s]", "", output)
    file_content = re.sub(r"\b\d+\b", "", file_content)

    words = word_tokenize(file_content)
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word not in stop_words]

    tagged_words = nltk.pos_tag(filtered_words)
    vocabulary_list = [word for word, pos in tagged_words if pos not in ["NNP", "CD"]]

    vocabulary_list = list(set(vocabulary_list))
    vocabulary_list_string = "['" + "', '".join(vocabulary_list) + "']"
    print("Processed result: " + vocabulary_list_string[0: 10] + "...")

    return vocabulary_list_string
  

  def finalize_output(self, prompt, data=None):
    try:
      response = client.chat.completions.create(
        model=self.model,
        messages=[
            { "role": "system", "content": self.system_context },
            { "role": "user", "content": [{ "type": "text",  "text": prompt + data if data else prompt}]}
        ],
        temperature=1.0,
        max_tokens=3500
      )
    except Exception as e:
      print(f"Error: {e}")
      return None
    return response


  def abstract_vocab_from_image(self, image_path, prompt, system_context=None):
    encoded_images = []

    with open(image_path, "rb") as image_file:
      encoded_paragraph = base64.b64encode(image_file.read()).decode('utf-8')
      encoded_images.append(encoded_paragraph)
    
    print("--- Number of paragraph encoded: " + str(len(encoded_images)) + " ---")

    try:
      response = client.chat.completions.create(
        model=self.model,
        messages=[
          { "role": "system", "content": system_context if system_context != None else self.system_context },
          { "role": "user", "content": [
              { "type": "text", "text": prompt },
              { "type": "image_url", "image_url": { "url": f"data:image/png;base64,{encoded_images[0]}" } }        
          ]}
        ],
        temperature=1.0,
        max_tokens=3500
      )
      
    except Exception as e:
      print(f"Error: {e}")
      return None
    
    return response


  def start_process(self, image_path):
    output = self.preprocess(self.abstract_vocab_from_image(image_path, self.default_prompt, system_context=SYSTEM_CONTEXT_TEACHER))
    user_prompt = VERB_PROMPT + " " + output
    response = self.finalize_output(user_prompt)
    response_text = response.choices[0].message.content
    response = response_text.replace("\n", "")
    if response:
      output = json.loads(response)
    return output
  

  def fetch_qa_from_image(
      self,
      passage_image_path=f"{root}/sample_textbook_images/p1.png", 
      question_image_path=f"{root}/sample_textbook_images/q1.jpg", 
      answer_image_path=f"{root}/sample_textbook_images/a1.jpg"
    ):

    print("Start to process the reading paragraph...")
    fetched_p = self.abstract_vocab_from_image(passage_image_path, FETCH_PARAGRAPH)
    reading_paragraph = self.preprocess(fetched_p)
    print("Paragraph: " + reading_paragraph)
    time.sleep(5)

    print("Start to process the questions...")
    fetched_q = self.abstract_vocab_from_image(question_image_path, FETCH_QUESTIONS)
    questions = self.preprocess(fetched_q)
    print("Questions " + questions)
    time.sleep(5)

    print("Start to process the answers...")
    fetched_a = self.abstract_vocab_from_image(answer_image_path, FETCH_ANSWERS)
    answers = self.preprocess(fetched_a)
    print("Correct answers: " + answers)
    time.sleep(5)
    
    data = f"Paragraph: {str(reading_paragraph)} <===> Questions: {str(questions)} <===> Answers: {str(answers)}"
    pdb.set_trace(header="...Processing...")
   
    analysis = self.finalize_output(ANALYZE_QA, data)
    final_output = self.preprocess(analysis)
    print("Final outcome: " + final_output)

    return final_output
