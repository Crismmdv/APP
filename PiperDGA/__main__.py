from . import app
import webview

if __name__=="__main__":

    window=webview.create_window('APPiper',app)
    #app.run()
    webview.start()