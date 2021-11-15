# import time module, Observer, FileSystemEventHandler
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import socket
import sys
import os

ip = sys.argv[1]
port = int(sys.argv[2])
path = sys.argv[3]
timer = sys.argv[4]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

if len(sys.argv) == 5:
    client_id = sys.argv[5]
else:
    s.send(bytes("path", path))
    client_id = s.recv(128)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))


class OnMyWatch:
    # Set the directory on watch
    watchDirectory = path

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            print("Watchdog received modified event - % s." % event.src_path)


if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()

# msg = b'Ron and Aviv Harel'
# s.send(msg)
# data = s.recv(100)
# print("Server sent: ", data)

# if data == msg.upper():
#     msg = b'308433762 318174950'
#     s.send(msg)
#     data = s.recv(100)
#     print("Server sent: ", data)

s.close()
