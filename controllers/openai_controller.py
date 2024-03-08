from openai import OpenAI
import os

class OpenAiAPI:

  def __init__(self):
    GPT_35_MODEL_NAME = 'gpt-3.5-turbo-instruct'
    GPT_4_MODEL_NAME = 'gpt-4'
    self.key = os.environ.get('OPENAI_KEY')
    self.model = GPT_4_MODEL_NAME
    self.gpt = OpenAI(api_key=self.key)

  def query_chat(self, prompt):
    print("querying")
    response = self.gpt.chat.completions.create(
            model=self.model,
            messages=[
              {
              "role": "user",
              "content": prompt
              }
            ] 
        )
    print(response.choices[0].message.content)
    return response.choices[0].message.content