# import time module, Observer, FileSystemEventHandler
import time


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import socket
import sys
import os
CHUNKSIZE = 1_000_000

ip = sys.argv[1]
port = int(sys.argv[2])
src_path = sys.argv[3]
timer = int(sys.argv[4])


class OnMyWatch:
    # Set the directory on watch
    watchDirectory = src_path

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(timer)
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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

if len(sys.argv) == 6:
    client_id = sys.argv[5]
else:
    # send the file in the path to the sever.
    s.send((b"path"+src_path.encode()))

    ##################################################################33
    while True:
        with s:
            for path, dirs, files in os.walk(src_path):
                for file in files:
                    filename = os.path.join(path, file)
                    relpath = os.path.relpath(filename, 'src_path')
                    filesize = os.path.getsize(filename)

                    print(f'Sending {relpath}')

                    with open(filename, 'rb') as f:
                        s.sendall(relpath.encode() + b'\n')
                        s.sendall(str(filesize).encode() + b'\n')

                        # Send the file in chunks so large files can be handled.
                        while True:
                            data = f.read(CHUNKSIZE)
                            if not data: break
                            s.sendall(data)
    #############################################################33
    client_id = s.recv(128)

watch = OnMyWatch()
watch.run()


# if __name__ == '__main__':
#     watch = OnMyWatch()
#     watch.run()

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
