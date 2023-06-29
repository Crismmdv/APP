from PiperDGA import app
import webview
from flaskwebgui import FlaskUI
#CORS(app)

if __name__ =="__main__":
    app.run()
    
    ### Ativar para app en ventana. Desactivar para server.
    #FlaskUI(app=app, server="flask").run()
    # #window=webview.create_window('APPiper',app)
    #webview.start()