from PyQt5.QtCore import pyqtSignal, QThread
import os,pickle,re,requests,pytchat
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import threading
class YouTubeAPI(QThread):
    updateListWidget = pyqtSignal(str)
    def __init__(self,args, index=0):
        QThread.__init__(self)
        self.args = args
        self.index = index
    def login(self):
        SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
        creds = None
        path = self.args.ui.lineEdit.text()
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
    def getIDVideo(self):
        return str(re.findall('v=(.*)',requests.get(self.args.ui.lineEdit_2.text()).url)[0])
    def getLiveChatID(self):
        api_key = 'AIzaSyDNchT4xvqof0DpPIjpdsxRHQM4N9MUZts'
        youtube = build('youtube','v3', developerKey = api_key)
        res = youtube.videos().list(id=self.getIDVideo(),
                            part='snippet,contentDetails,liveStreamingDetails').execute()
        return res.get('items')[0].get('liveStreamingDetails').get('activeLiveChatId')
    def commentYoutube(self):
        liveChatId = self.getLiveChatID()
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
        youtube = build('youtube', 'v3', credentials=creds)
        youtube.videos().rate(rating='like', id=self.getIDVideo()).execute()
        request = youtube.liveChatMessages().insert(
            part="snippet",
                body={
                    "snippet": {
                    "liveChatId": liveChatId,
                    "type": "textMessageEvent",
                    "textMessageDetails": {
                    "messageText": f"{self.args.ui.lineEdit_3.text()}"
                    }
                }
            }
        )
        response = request.execute()
        # print(response)
    def getMessageLivechat(self):
        chat = pytchat.create(video_id=self.getIDVideo())
        while chat.is_alive():
            for c in chat.get().sync_items():
                self.updateListWidget.emit(f"{c.datetime} [{c.author.name}]- {c.message}")
                print(f"{c.datetime} [{c.author.name}]- {c.message}")
    def run(self):
        self.listThread = []
        if self.index == 0:
            self.login()
        if self.index == 1:
            self.getMessageLivechat()
        if self.index == 2:
            new_Thread = threading.Thread(target=self.commentYoutube, args=())
            self.listThread.append(new_Thread)
            for x in self.listThread:
                x.start()
        self.exec_()