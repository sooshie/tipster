import threading
import time
import itertools
from iocextract import extract_emails, extract_hashes, extract_ips, extract_urls

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

def submit_iocs_window(parent, iocs):
    dialogWindow = Gtk.Window()
    dialogWindow.set_title("Submit IOCs")


    def on_submit_clicked(button, buff):
        start_iter = buff.get_start_iter()
        end_iter = buff.get_end_iter()
        text = buff.get_text(start_iter, end_iter, True)
        submit_iocs = [i.strip() for i in text.split('\n')]
        print(submit_iocs)


    def on_cancel_clicked(button):
        print("Closing application")
        dialogWindow.destroy()

    grid = Gtk.Grid()
    dialogWindow.add(grid)

    sw = Gtk.ScrolledWindow()
    max_w = 0
    for i in iocs:
        if len(i) > max_w:
            max_w = len(i)
    sw.set_size_request(max_w * 8, 100)
    sw.set_hexpand(True)
    sw.set_vexpand(True)
    grid.attach(sw, 0, 1, 3, 1)

    tv = Gtk.TextView()
    buff = tv.get_buffer()
    buff.set_text("\n".join(iocs))
    sw.add(tv)

    submit = Gtk.Button.new_with_mnemonic("_Submit")
    submit.connect("clicked", on_submit_clicked, buff)
    grid.attach(submit, 0, 2, 1, 1)

    cancel = Gtk.Button.new_with_mnemonic("_Cancel")
    cancel.connect("clicked", on_cancel_clicked)
    grid.attach_next_to(cancel, submit, Gtk.PositionType.RIGHT, 1, 1)

    dialogWindow.show_all()


class MainWindow(Gtk.Window):


    def __init__(self):
        super(MainWindow, self).__init__()
      
        self.set_title("Tipster - I'm here to help!")
        image1 = Gtk.Image()
        image1.set_from_file("clippy.png")
        self.add(image1)


    def submit_iocs(self, iocs):
        return submit_iocs_window(self, iocs)


def app_main():
    iocs = []
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()


    def iter_check(iterable):
        try:
            first = next(iterable)
        except StopIteration:
            return None
        return itertools.chain([first], iterable)


    def check_clippy(iocs):
        last_text = ''

        while True:
            iocs_found = False
            urls, ips, emails, hashes = None, None, None, None
            text = clipboard.wait_for_text()

            # If there's text and it has not already been parsed
            if text is not None and text != last_text:
                urls = iter_check(extract_urls(text, refang=True))
                if urls is not None:
                    iocs = iocs + [u for u in urls]
                    iocs_found = True

                ips = iter_check(extract_ips(text, refang=True))
                if ips is not None:
                    iocs = iocs + [i for i in ips]
                    iocs_found = True
                
                emails = iter_check(extract_emails(text, refang=True))
                if emails is not None:
                    iocs = iocs + [e for e in emails]
                    iocs_found = True

                hashes = iter_check(extract_hashes(text))
                if hashes is not None:
                    iocs = iocs + [h for h in hashes]
                    iocs_found = True

                if iocs_found:
                    GLib.idle_add(win.submit_iocs, list(set(iocs)))

            iocs = []
            last_text = text
            time.sleep(1)

    thread = threading.Thread(target=check_clippy, args=(iocs, ))
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    app_main()
    Gtk.main()
