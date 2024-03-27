import requests
from decorators.service import service
import re
from services.gemini import GeminiService

@service()
class DiscordService():
    __token = None
    __gemini_service = GeminiService.get_instance()
    __messages = []
    __users = []
    __lastMessages = 0


    def __constructor__(self) -> None:
        self.__token = 'MzQzNDM1MjE2NzUwMjQ3OTQ3.Gb2Zxf.MoyRr3E_4dHNKH5ASlauFpR-3uwHmy5CjD_XW4'

    def read_messages(self):
        response = requests.get(url='https://discord.com/api/v9/channels/1048966015268180019/messages?limit=50',headers={"Authorization":self.__token})
        if response.status_code == 200:
            return  [{'uuid':message.get('author').get('id'),'autor':message.get('author').get('username')} for message in response.json()],[{'autor':message.get('author').get('username'),'content':message.get('content'),'mentions':message.get('mentions'),'reference':message.get('referenced_message').get('author').get('username') if message.get('referenced_message') else None} for message in response.json()]
        
    def update_repo(self):
        users, messages = self.read_messages()
        for user in users:
            if user not in self.__users:
                self.__users.append(user)
        
        regex_pattern = r'<@(\d+)>'
        for message in messages:
            if message not in self.__messages:
                matches = re.findall(regex_pattern, message.get('content'))
                for number in [match for match in matches]:
                    for user in self.__users:
                        if user.get('uuid') == number:
                            message['content'] = message.get('content').replace('<@'+number+'>',user.get('autor'))
                self.__messages.append(message)

    def has_new_messages(self):
        if self.__lastMessages != len(self.__messages):
            for x in range(0,(len(self.__messages) - self.__lastMessages)):
                self.__lastMessages = self.__lastMessages +1 
                message = self.__messages[x]
                if len(message.get('mentions')) > 0 and 'szortownik' in [user.get('username') for user in message.get('mentions')]:
                    print(message.get('content'))
                    print(self.__gemini_service.generate_message("Wybraź sobie że jesteś forumowym chamskim i bezczelnym hejterem i masz na imię szortownik. Używasz dużo sarkazmu, wulgarnych słów i obelg. Odpowiadsz tylko jednym lub dwoma zdaniami, zawsze negatywnie w stosunku do opini podanej opini niżej:"+message.get('content')))