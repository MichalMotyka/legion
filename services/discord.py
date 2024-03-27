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
        response = requests.get(url='https://discord.com/api/v9/channels/537601821339025410/messages?limit=10',headers={"Authorization":self.__token})
        if response.status_code == 200:
            return  [{'uuid':message.get('author').get('id'),'autor':message.get('author').get('username')} for message in response.json()],[{"uuid":message.get('id'),'autor':message.get('author').get('username'),'content':message.get('content'),'mentions':message.get('mentions'),'reference':message.get('referenced_message').get('author').get('username') if message.get('referenced_message') else None,"read":False} for message in response.json()]
     
    def update_repo(self):
        print('update_repo')
        users, messages = self.read_messages()
        for user in users:
            if user not in self.__users:
                self.__users.append(user)
        
        regex_pattern = r'<@(\d+)>'
        for message in messages:
            if message.get('uuid') not in [msg.get('uuid') for msg in self.__messages]:
                print("tu jestem")
                matches = re.findall(regex_pattern, message.get('content'))
                for number in [match for match in matches]:
                    for user in self.__users:
                        if user.get('uuid') == number:
                            message['content'] = message.get('content').replace('<@'+number+'>',user.get('autor'))
                            if message.get('autor') == "szortownik":
                                message["read"] = True
                self.__messages.append(message)

    def __send_message(self,message):
        body = {"mobile_network_type":"unknown","content":message,"nonce":"","tts":False,"flags":0}
        requests.post(url='https://discord.com/api/v9/channels/537601821339025410/messages',data=body,headers={"Authorization":self.__token})

    def has_new_messages(self):

        print('has_new_messages')
        for message in self.__messages:
            print(not message.get("read") and len(message.get('mentions')) > 0 and 'szortownik' in [user.get('username') for user in message.get('mentions')])
            if not message.get("read") and len(message.get('mentions')) > 0 and 'szortownik' in [user.get('username') for user in message.get('mentions')]:
                self.__send_message(self.__gemini_service.generate_message("Wybraź sobie że jesteś forumowym chamskim i bezczelnym hejterem. Używasz dużo sarkazmu, wulgarnych słów i obelg. Odpowiadsz tylko jednym lub dwoma zdaniami, zawsze negatywnie w stosunku do opini podanej opini niżej:"+message.get('content')))
                message["read"] = True