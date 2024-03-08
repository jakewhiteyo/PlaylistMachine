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
    response = self.gpt.chat.completions.create(
            model=self.model,
            messages=[
              {
                "role":"system",
                "content": "You are a resource for generating SEO optimized Spotify playlists titles, I will give you a list of Reddit post titles declaring upcoming things like concerts and song/album releases and you will respond with a SEO playlist name related to the title. For example, if there is a post announcing a new childish gambino album called 2005, you would make a playlist name called \“2005 by Childish Gambino\”, dont add too much, only what someone might search. If the post title is not related to upcoming concerts or a song/album announcement, just skip that one and don’t respond with anything. If it mentions an album or song in the title, assume it is an announcement and generate a playlist name for it. Respond to this prompt with a list of potential SEO optimized spotify playlist names that relate to the announcements."
              },
              {
              "role": "user",
              "content": prompt
              }
            ] 
        )
    return response.choices[0].message.content