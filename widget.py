import gi
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit', '3.0')
from gi.repository import WebKit, Gtk, Gdk, Gio, GLib
import signal,os

file_url = os.path.dirname(os.path.abspath(__file__)) + '/widget.html'

class MainWin(Gtk.Window):
    def __init__(self,address="127.0.0.1", port=54541):
        Gtk.Window.__init__(self, skip_pager_hint=True, skip_taskbar_hint=True)
        self.set_wmclass("sildesktopwidget","sildesktopwidget")
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_size_request(400,400)
        self.set_keep_below(True)

        #Set transparency
        screen = self.get_screen()
        rgba = screen.get_rgba_visual()
        self.set_visual(rgba)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0,0,0,0))

        #Add all the parts
        self.view = WebKit.WebView()
        self.view.set_transparent(True)
        self.view.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0,0,0,0))
        self.view.props.settings.props.enable_default_context_menu = False
        self.view.load_uri("file://"+file_url)

        box = Gtk.Box()
        self.add(box)
        box.pack_start(self.view, True, True, 0)
        self.set_decorated(False)
        self.connect("destroy", lambda q: Gtk.main_quit())

        s = Gdk.Screen.get_default()
        w = s.get_width()
        h = s.get_height()
        #Show all the parts
        self.show_all()
        self.move(w-450,100)

class Logger:
    def __init__(self, root):
        self.root = root
        self.log("Logger loaded")

    def log(self, msg, level='console'):
        if level=='console':
            print msg


class App(object):
    """docstring for App"""
    def __init__(self, arg=False):
        self.log = Logger(self).log
        self.gio_file = Gio.File.new_for_path(file_url)
        self.monitor = self.gio_file.monitor_file(Gio.FileMonitorFlags.NONE, None)
        self.monitor.connect("changed", self.file_changed)

        self.mainwin = MainWin()
        signal.signal(signal.SIGINT, signal.SIG_DFL) # make ^c work
    
    def run(self):
        Gtk.main()

    def file_changed(self,monitor, file, unknown, event):
        # reload
        GLib.timeout_add_seconds(2, self.refresh_file)


    def refresh_file(self,*args):
        self.mainwin.view.reload()
        

if __name__ == '__main__':
    app = App()
    app.run()