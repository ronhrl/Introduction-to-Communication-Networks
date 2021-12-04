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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        print("45")
        s.sendall(client_id)
        if event.is_directory:
            return None

        #name = os.path.basename(event.src_path)
        filename = event.src_path
        print(filename)
        relpath = os.path.basename(event.src_path)
        print(relpath)
        filesize = os.path.getsize(filename)
        print(filesize)

        print(f'Sending {relpath}')

        with open(event.src_path, 'rb') as f:
            s.sendall(relpath.encode() + b'\n')
            s.sendall(str(filesize).encode() + b'\n')
            print("63")
            # Send the file in chunks so large files can be handled.
            while True:
                data = f.read(CHUNKSIZE)
                print("67")
                if not data:
                    break
                s.sendall(data)
                print("70")

        # print("Watchdog received created event - % s." % event.src_path)

        # elif event.event_type == 'modified':
        #     # Event is modified, you can process it now
        #     print("Watchdog received modified event - % s." % event.src_path)


print("78")
i = 0
if len(sys.argv) == 6:
    client_id = sys.argv[5]
    # s.sendall("hello".encode())
    # data1 = s.recv(100)
    # print(data1)
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # send the file in the path to the sever.
    s.send(b"path")
    client_id = s.recv(128)
    print(client_id)
    ##################################################################33
    with s:
        for path, dirs, files in os.walk(src_path):
            print("#############################")
            print(src_path)
            print(path)
            print(dirs)
            print(files)
            print("#############################")
            for file in files:
                filename = os.path.join(path, file)
                print(filename)
                relpath = os.path.relpath(filename, src_path)
                print(relpath)
                filesize = os.path.getsize(filename)
                print(filesize)
                print(f'Sending {relpath}')

                with open(filename, 'rb') as f:
                    print(i)
                    i += 1
                    s.sendall(relpath.encode() + b'\n')
                    s.sendall(str(filesize).encode() + b'\n')

                    # Send the file in chunks so large files can be handled.
                    while True:
                        data = f.read(CHUNKSIZE)
                        if not data: break
                        s.sendall(data)
    #############################################################

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
