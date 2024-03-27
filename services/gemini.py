import google.generativeai as genai
from decorators.service import service

@service()
class GeminiService():

    def __constructor__(self) -> None:
        genai.configure(api_key='AIzaSyDeTUqV2GL78KAsEKaJzXS3I8JD6HFopiw')
    
    def generate_message(self,message:str) -> str:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(message)
        return response.text