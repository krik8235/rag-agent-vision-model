DEFAULT_USER_PROMPT = """
This is complete vertically stacked image of multiple consecutive ordered pages of an IELTS reading passage. Your task is to carefully analyze the image and extract all the text from it. The passages are long so thats why whole passage is given to you in a form of vertically stiched one picture.

STRICT IMPORTANT NOTE: I NEED EXTRACTED DATA IN THE FORMAT THAT I AM SAYING TO YOU WITHOUT ANY EXPLANATIONS OR SUGGESTIONS FROM YOUR SIDE. I AM A PROGRAMMER AND I WILL USE YOUR OCR EXTRACTED TEXT IN MY APPLICATION. I NEED ONLY REQUIRED EXTRACTED DATA FROM YOU AND NOTHING ELSE.

Some visual cues to assist you in this process:
1- There are most probably instructions too for the students to read the passage(they are mostly in the start of the picture), i also need those instructions.
2- The largest and boldest text at the top of the picture is likely the title of the passage.
3- If there is a subtitle present that will always be below the main title of the passage, although sometimes a subtitle is absent for the passage and not provided by the IELTS.
4- Heading and subtitle are always relevant to each other and they describe an overall idea about the text in the main body of the passage.
5- Following the heading (and potential subtitle), you'll find the main body of the passage. When you are extracting the text from the main body make sure you keep the format of paragraphs the same as depicted in the picture. for every start of new paragraph insert a '\n' (line break), so that my parser later understand that this is the start of a new paragraph. There can be a case where a half portion of the last paragraph is in the first page and the other remaining half is at the start of the second page, which means a parapraph might continue to the next page but it is only one paragraph as a whole.
6- According to official IELTS website the reading passages have 2000-3000 words in the main body as a whole.

Please extract all my mentioned and required details from the image, as I will conduct further analysis on it afterward.

Please deeply analyze the full text of the passage and return it in the following JSON format: 
{
    "instructions": "Instruction by IELTS (if present otherwise write None)",
    "title": "Extracted Title Here",
    "subtitle": "Extracted Subtitle Here (if present otherwise write None)",
    "text": "Full text of the passage here."
}
"""


VERB_PROMPT = """
You are an expert English teacher. You know about the grammar rules and have extensive knowledge of English literature. You have to analyze the given words in depth and find relations. Your goal is to provide a list of words that I can use in my IELTS English speaking and writing tasks to improve my vocabulary. Ignore the words in the array that cannot be used in conversations.

NOTE: YOU HAVE TO FOLLOW THE STRICT GUIDELINES GIVEN TO YOU AND RETURN THE REQUIRED ANSWER IN THE SPECIFIED FORMAT AT THE END OF THIS PROMPT. PROVIDE THE DATA IN JSON FORMAT, AND NOTHING ELSE. I WILL USE THE OUTPUT DIRECTLY IN MY APPLICATION, SO IT MUST BE STRICTLY IN JSON.

Specifically, focus on these things:
1 - Group the words that have similar or closely related meanings, and ensure these words can be used in both English speaking and writing. Make at least 10 groups of words, each containing a maximum of 5 words or a minimum of 1.
2 - Generate a vivid meaning of each word that is relevant to the English dictionary.
3 - For speaking, group semi-formal words together.
4 - For writing, group formal words that can be used in formal English writing.
5 - Once the grouping of words is complete, craft one sentence for each word: one for formal academic writing.
6 - Also, ensure that the two generated sentences for each word are linked together, so it is easy for students to grasp the meaning of the word and use it in different contexts.

In this way, students can learn more English words intuitively, and it will remain in their heads for a long time.

OUTPUT FORMAT:
Please return the data in JSON format with the following structure:

{
  "groups": [
    {
      "id": "<group_id>",
      "words": [
        {
          "word": "<word>",
          "meaning": "<meaning in English literature>",
          "sample": "<formal academic sentence>",
        },
        ...
      ]
    },
    ...
  ]
}

ARRAY OF ENGLISH WORDS:
"""



FETCH_PARAGRAPH = """
You will be provided with image containing paragraphs. Follow the instruction below and return your output:

Instructions:
1. Extract and return all paragraphs from the image.
2. Maintain the exact formatting as shown in the image.
3. Output strictly in JSON format.

Output format:
{
  "paragraphs": "<Extracted paragraph 1>",
}

"""


FETCH_QUESTIONS = """
You will be provided with image containing questions. Follow the instruction below and return your output:

1. Identify Questions:
   - Identify the instructions and ignore them.
   - Extract only the questions, ignoring any instructions or rules given.
   - If a set of rules (e.g., "TRUE/FALSE/NOT GIVEN") is provided before the questions, exclude the rules and focus solely on the questions.
   - Identify each question type based on instructions given.
   - Strictly remove the instructions from output and fetch questions only

2. Numbering Questions:
   - Identify the index of each question, it mainly starts from 1.
   - Continue numbering sequentially across multiple images if questions span across multiple images.
   - Return the extracted text in the following JSON format without providing any explanation.

3. Output Format:
  
   {
    "Questions": {
    "1": "<Extracted question 1>",
    "2": "<Extracted question 2>",
    "...": "<Extracted question N>"
    }
   }
"""


FETCH_ANSWERS = """
You will be provided with image containing solutions. ollow the instruction below and return your output:

1. Identify Answers:
   - Extract only the answers starting from index 1 if given, ignoring any instructions or rules provided.

2. Numbering Answers:
   - Identify the index to each answers.
   - Continue numbering sequentially.
   - Return the extracted text in the following JSON format without providing any explanation.

3. Output Format:

   {
        "1": "<Extracted answer 1>",
        "2": "<Extracted answer 2>",
        "...": "<Extracted answer N>"
    }
   
"""


ANALYZE_QA = """
You are an expert in text analysis and comprehension. You will be provided with a paragraph, a set of questions, and corresponding answers separated by "<===>". Your task is to analyze the provided text and fulfill the following requirements:

1. Extract the full paragraph and identify its structure, noting the specific locations of information (e.g., "paragraph 3, line 4").

2. For each question, provide:
   - The question index (e.g., 1, 2, 3, etc.).
   - The corresponding answer from the solution.
   - A clear and concise reasoning for why that specific answer was selected, referencing relevant parts of the paragraph.
   - The location of the relevant information in the paragraph (e.g., "paragraph 2, line 3").
   - Return the extracted text in the following JSON format:

3. Output Format:
  
{
  "answers": {
    "1": {
      "answer": "<Corresponding answer for question 1>",
      "reasoning": "<Reason for the answer based on the paragraph>",
      "location": "<Location in the paragraph (e.g., 'paragraph 2, line 3')>"
    },
    "2": {
      "answer": "<Corresponding answer for question 2>",
      "reasoning": "<Reason for the answer based on the paragraph>",
      "location": "<Location in the paragraph (e.g., 'paragraph 3, line 5')>"
    },
    "...": {
      "answer": "<Corresponding answer for question N>",
      "reasoning": "<Reason for the answer based on the paragraph>",
      "location": "<Location in the paragraph (e.g., 'paragraph 4, line 2')>"
    }
  }
}
"""