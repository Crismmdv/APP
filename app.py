from PiperDGA import app
import webview
from flaskwebgui import FlaskUI
#CORS(app)
window=webview.create_window('APPiper',app)
if __name__ =="__main__":
    #app.run()
    #webview.create_window('Hello world', 'http://127.0.0.1:5000')
    webview.start()
    #FlaskUI(app=app, server="flask").run()