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
client = Together(api_key=together_api_key)

filename = sys.argv[0]
root_dir = os.path.dirname(__file__)

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


  def create_vocab_list(self, model_res) -> str:
    print("Start to create a vocabulary list from the model output")

    output = ""
    if model_res and hasattr(model_res, "choices"):
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

  def extract_vocab_from_image(self, image_path, prompt, system_context=None):
    encoded_images = []

    with open(image_path, "rb") as image_file:
      encoded_paragraph = base64.b64encode(image_file.read()).decode('utf-8')
      encoded_images.append(encoded_paragraph)
    
    print("--- Number of paragraph encoded: " + str(len(encoded_images)) + " ---")

    try:
      response = client.chat.completions.create(
        model=self.model,
        messages=[
          { "role": "system", "content": self.system_context if system_context == None else system_context },
          { "role": "user", "content": [
              { "type": "text", "text": prompt },
              { "type": "image_url", "image_url": { "url": f"data:image/png;base64,{encoded_images[0]}" } }        
          ]}
        ],
        temperature=0.7,
        max_tokens=3000,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>","<|eom_id|>"],
      )
    
    except Exception as e:
      print(f"Error: {e}")
      return None
    
    return response


  def finalize_output(self, prompt, data=None):
    try:
      response = client.chat.completions.create(
        model=self.model,
        messages=[
            { "role": "system", "content": self.system_context },
            { "role": "user", "content": [{ "type": "text",  "text": prompt if data == None else prompt + data}]}
        ],
        temperature=0.7,
        max_tokens=3500,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>","<|eom_id|>"],
      )
    
    except Exception as e:
      print(f"Error: {e}")
      return None
    
    return response


  def start_process(self, image_path):
    model_output =self.extract_vocab_from_image(image_path, self.default_prompt, SYSTEM_CONTEXT_TEACHER)
    vocab_list = self.create_vocab_list(model_output)
    user_prompt = VERB_PROMPT + " " + vocab_list
    response = self.finalize_output(prompt=user_prompt)
    if response and hasattr(response, "choices"):
      response_text = response.choices[0].message.content.strip().replace("\n", "").strip("<b>").strip("</b>").lower()
      return response_text
    
    return None
  

  def fetch_qa_from_image(
      self,
      passage_image_path=f"{root_dir}/sample_textbook_images/p1.png", 
      question_image_path=f"{root_dir}/sample_textbook_images/q1.jpg", 
      answer_image_path=f"{root_dir}/sample_textbook_images/a1.jpg"
    ):

    print("Start to process the paragraph...")
    fetched_p = self.extract_vocab_from_image(image_path=passage_image_path, prompt=FETCH_PARAGRAPH)
    reading_paragraph = self.create_vocab_list(fetched_p)
    print("Paragraph: " + reading_paragraph)
    time.sleep(5)

    print("Start to process the questions...")
    fetched_q = self.extract_vocab_from_image(image_path=question_image_path, prompt=FETCH_QUESTIONS)
    questions = self.create_vocab_list(fetched_q)
    print("Questions " + questions)
    time.sleep(5)

    print("Start to process the answers...")
    fetched_a = self.extract_vocab_from_image(image_path=answer_image_path, prompt=FETCH_ANSWERS)
    answers = self.create_vocab_list(fetched_a)
    print("Correct answers: " + answers)
    time.sleep(5)
    
    data = f"Paragraph: {str(reading_paragraph)} <===> Questions: {str(questions)} <===> Answers: {str(answers)}"
    pdb.set_trace(header="...Processing the final reult...")
   
    analysis = self.finalize_output(ANALYZE_QA, data)
    final_output = self.create_vocab_list(analysis)
    print("Final outcome: " + final_output)

    return final_output
