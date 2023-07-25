from .endpoints import Endpoints
from emoji import demojize
vid = input("Enter your stream link: ")

class Startup:

    @staticmethod
    def run():
        endpoint = Endpoints()
        token = endpoint.getChatToken()

        cid = token["conversations"][0]["cid"]

        def formatMessage(username, message):
            response = "[yt] " + username + ': ' + message
            return demojize(response)

        def sendMessage(username,message):
            printable = formatMessage(username, message)
            endpoint.postNewChatMessage(cid, printable)

        endpoint.startYoutubeChat(vid,sendMessage)
