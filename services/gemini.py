import google.generativeai as genai
from decorators.service import service

@service()
class GeminiService():
    __safe = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    def __constructor__(self) -> None:
        genai.configure(api_key='AIzaSyDeTUqV2GL78KAsEKaJzXS3I8JD6HFopiw')
    
    def generate_message(self,message:str) -> str:
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(message,safety_settings=self.__safe)
            return response.text
        except Exception as e:
            print(e)