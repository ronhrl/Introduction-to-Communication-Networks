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
        # print("event")
        # When event is accord create new socket to upload the change.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        # print(type(client_id))
        if type(client_id) is bytes:
            # print("bytes")
            s.sendall(client_id)
        else:
            s.sendall(client_id.encode())
        print(client_id)
        # s.sendall(client_id.encode())
        if event.is_directory:
            return None
        if event.event_type == 'deleted':
            print(b'delete!'+event.src_path.encode() + b'\n')
            s.sendall(b'delete!'+event.src_path.encode() + b'\n')
        elif event.event_type == 'modified':
            pass
        else:
            #name = os.path.basename(event.src_path)
            filename = event.src_path
            print(filename)
            relpath = os.path.basename(event.src_path)
            print(relpath)
            filesize = os.path.getsize(filename)
            print(filesize)
            print(f'Sending {relpath}')
            assert os.path.isfile(event.src_path)
            with open(event.src_path, 'rb') as f:
                s.sendall(relpath.encode() + b'\n')
                s.sendall(str(filesize).encode() + b'\n')

                # Send the file in chunks so large files can be handled.
                while True:
                    data = f.read(CHUNKSIZE)
                    if not data:
                        break
                    s.sendall(data)

        # print("Watchdog received created event - % s." % event.src_path)

        # elif event.event_type == 'modified':
        #     # Event is modified, you can process it now
        #     print("Watchdog received modified event - % s." % event.src_path)


print()
i = 0
if len(sys.argv) == 6:
    client_id = sys.argv[5]
    print("################" + client_id)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.sendall(("first" + client_id).encode())
    # s.sendall(client_id.encode())
    with s.makefile('rb') as clientfile:
        while True:
            raw = clientfile.readline()
            # print("raw")
            # print(raw)
            # if "done" in raw:
            #     break
# #             if not raw:
#             # s.send(b'done')
#                 s.close()
#                 break  # no more files, server closed connection.

            filename = raw.strip().decode()
            if "done" in filename:
                break
            if not raw:
                continue
            length = int(clientfile.readline())
            print(f'Downloading {filename}...\n  Expecting {length:,} bytes...', end='', flush=True)
            # data_list.append(filename)
            # data_hash[rand_id] = data_list
            # print("**************")
            # print(data_hash[rand_id])
            # print("**************")
            dir_name = str(src_path).split("\\")[-1]
            # print("#########")
            # print(dir_name)
            # print("#########")
            path = os.path.join(src_path, filename)
            # os.makedirs(os.path.dirname(path), exist_ok=True)

            # Read the data in chunks so it can handle large files.
            with open(path, 'wb') as f:
                while length:
                    print(110)
                    chunk = min(length, CHUNKSIZE)
                    data = clientfile.read(chunk)
                    # print("@@@@@@@@@@")
                    # print(data)
                    # print("@@@@@@@@@@")
                    if not data:
                        break
                    f.write(data)
                    length -= len(data)
                else:  # only runs if while doesn't break and length==0
                    print('Complete')
                    continue
                    # break

    # print("Close")
    # s.close()
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # send the file in the path to the sever.
    s.send(b"path")
    client_id = s.recv(128)
    ##################################################################33
    with s:
        for path, dirs, files in os.walk(src_path):
            print(src_path)
            print(path)
            print(dirs)
            print(files)
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
    #############################################################33

print("close")

watch = OnMyWatch()
# When the client finish to upload all the files, close the socket.
s.close()
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


