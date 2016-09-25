import gi
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit', '3.0')
from gi.repository import WebKit, Gtk, Gdk, Gio, GLib
import signal,os

class BackgroundPaneCallbacks:
    pass

class BackgroundPaneWebview(WebKit.WebView):
    def __init__(self):
        WebKit.WebView.__init__(self)
        self.set_transparent(True)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0,0,0,0))
        self.load_html_string('<HTML>'+\
                              '<STYLE type="text/css">'+\
                              'BODY { background: rgba(0,0,0,0);}'+\
                              '</STYLE>'+\
                              '<BODY>'+\
                              'Hello World'+\
                              '</BODY>'+\
                              '</HTML>',
                              'file:///')
        print("Webview loaded")

class BackgroundPaneWin(Gtk.Window):
    def __init__(self, address="127.0.0.1", port=54541):
        Gtk.Window.__init__(self)

        #Set transparency
        screen = self.get_screen()
        rgba = screen.get_rgba_visual()
        self.set_visual(rgba)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0,0,0,0))

        #Add all the parts
        self.view = BackgroundPaneWebview()
        box = Gtk.Box()
        self.add(box)
        box.pack_start(self.view, True, True, 0)
        self.set_decorated(False)
        self.connect("destroy", lambda q: Gtk.main_quit())
        #Configure   

        #Show all the parts
        self.show_all()


        print("Win loaded")

class BackgroundPane:
    def __init__(self, params=False):
        #Add all the parts
        self.root = params['root']
        self.win = BackgroundPaneWin()
        print("Pane loaded")

    def init(self):
        pass

    def add_widget(self, widget):
        pass

class Logger:
    def __init__(self, root):
        self.root = root
        self.log("Logger loaded")

    def log(self, msg, level='console'):
        if level=='console':
            print msg

class Handlers:
    pass

class App:
    def __init__(self, params={}):
        #Get screen geometry
        s = Gdk.Screen.get_default()
        params['w'] = s.get_width()
        params['h'] = s.get_height()

        #Store params
        self.params = params
        self.log = Logger(self).log
        self.handlers = Handlers()
        #Get all components
        bg = BackgroundPane({'root':self,
                                           })
        #Store all components
        self.components = {}
        self.components['bg'] = bg

        #Make sure everything is started

        #Make sure Ctl-C works
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def run(self):
        Gtk.main()

if __name__ == '__main__':
    print("Loading app...")
    app = App()
    app.run()