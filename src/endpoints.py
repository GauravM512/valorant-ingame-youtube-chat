import requests
import urllib3
from .exceptions import ValorantAPIError,YoutubeAPIError
from .auth import Auth
import pytchat

class Endpoints:

    def __init__(self) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        auth = Auth()
        self.headers = auth.getHeaders()
        self.config = auth.getConfig()
        self.port = self.config["port"]

    def __gameGetRequest(self, endpoint):
        response = requests.get(
            "https://127.0.0.1:{port}{endpoint}".format(
                port=self.port, endpoint=endpoint
            ),
            headers=self.headers,
            verify=False,
        )

        # custom exceptions for http status codes
        self.__verify_status_code(response.status_code)

        try:
            r = response.json()
            return r
        except:
            raise ValorantAPIError("An error ocurred trying to get game APIs")

    def __gamePostRequest(self, endpoint, data):
        response = requests.post(
            "https://127.0.0.1:{port}{endpoint}".format(
                port=self.port, endpoint=endpoint
            ),
            headers=self.headers,
            verify=False,
            json=data,
        )

        # custom exceptions for http status codes
        self.__verify_status_code(response.status_code)

        try:
            r = response.json()
            return r
        except:
            raise ValorantAPIError("An error ocurred trying to get game APIs")

    def __verify_status_code(self, status_code):
        """Verify that the request was successful according to exceptions"""
        if status_code in (404, 401, 500):
            raise ValorantAPIError(
                "An invalid status code returned from game APIs")

    def getChatToken(self):
        return self.__gameGetRequest("/chat/v6/conversations/ares-parties")

    def postNewChatMessage(self, cid, message):
        data = {
            "cid": cid,
            "message": message,
            "type": "system"
        }
        return self.__gamePostRequest("/chat/v6/messages", data)

    def startYoutubeChat(self,vid:str,callback):
        chat = pytchat.create(video_id=vid)
        while chat.is_alive():
            for c in chat.get().sync_items():
                if c.type=='superChat':
                    c.message = f"{c.message} [{c.amountString}]"
                if c.author.isChatModerator:
                    c.author.name = f"{c.author.name}[Mod]"
                if c.author.isChatOwner:
                    continue
                if c.author.isChatSponsor:
                    c.author.name = f"{c.author.name}[Sponsor]"
                callback(c.author.name,c.message)

        else:
            if chat.is_alive() == False:
                raise YoutubeAPIError("Please check if the stream is live and the video id is correct")