import socket
import string
import sys
import os
import random
from socket import *
import watchdog.events
import watchdog.observers
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CHUNKSIZE = 1_000_000
port = int(sys.argv[1])
id_dict = {}
server = socket(AF_INET, SOCK_STREAM)
server.bind(('', port))
data_hash = {}
data_list = []
delete_hash = {}
delete_list = []
rename_hash = {}
rename_dict = {}
new_client = 0
delete_flag = 0
server.listen(1)
while True:
    client_socket, client_address = server.accept()

    # print("##################")
    # print(client_address)
    # print(client_socket)
    # print("##################")
    # print("client")
    data = client_socket.recv(1024)
    print("data = " + data.decode())
    # print("#################")
    # print("data")
    # print(data)
    # print("#################")


    if b'update!' in data:
        rand_id = str(data).split("update!")[1][:-1]
        # print("rand id is - " + rand_id)
        server_path = os.getcwd()
        update_path = server_path + '\\' + rand_id
        delete_flag = 1
        i = 0
        # update only if the list is not empty.


        while len(data_list) != 0:
            print(data_list)
            for path, dirs, files in os.walk(update_path):
                    # print("the new path is : " + update_path)
                    # print(path)
                    # print(dirs)
                    # print(files)
                for file in files:
                    filename = os.path.join(path, file)
                        # print(filename)
                    relpath = os.path.relpath(filename, src_path)
                        # print(relpath)
                    filesize = os.path.getsize(filename)
                        # print(filesize)
                        #print(f'Sending {relpath}')
                        #print("file name - : " + file)
                    if file in data_list:
                        data_list.remove(file)
                        print("new list:")
                        print(data_list)
                        with open(filename, 'rb') as f:
                                # print(i)
                            i += 1
                            client_socket.sendall(relpath.encode() + b'\n')
                            client_socket.sendall(str(filesize).encode() + b'\n')

                                # Send the file in chunks so large files can be handled.
                            while True:
                                data = f.read(CHUNKSIZE)
                                if not data: break
                                client_socket.sendall(data)
        client_socket.close()
        continue

    elif b'delete!' in data:
        rand_id = str(data).split("delete!")[0][2:]
        delete_flag = 1
        remove_filename = os.path.basename(data.decode())
        server_path = os.getcwd()
        remove_path = server_path + '\\' + rand_id + '\\' + remove_filename
        delete_list.append(remove_filename)
        delete_hash[rand_id] = delete_list
        os.remove(remove_path[:-1])
        # if os.path.isfile(remove_path):
        #     os.remove(remove_path[:-1])
        # elif os.path.isdir(remove_path):
        #     os.rmdir(remove_path[:-1])
        client_socket.close()
        continue
    elif b'moved!' in data:
        rand_id = str(data).split("moved!")[0][2:]
        src_event = str(data).split("moved!")[1].split("dest")[0]
        dest_event = str(data).split("dest")[1][:-3]
        print("rand id: " + rand_id)
        print("src event: " +src_event)
        print("dest event: " +dest_event)
        delete_flag = 1
        src_filename = os.path.basename(src_event)
        dest_filename = os.path.basename(dest_event)
        print("src name: " + src_filename)
        print("dest name: " + dest_filename)
        server_path = os.getcwd()
        src_path = server_path + '\\' + rand_id + '\\' + src_filename
        dest_path = server_path + '\\' + rand_id + '\\' + dest_filename
        print("src path: " + src_path)
        print("dest path: " + dest_path)
        rename_dict[src_filename] = dest_filename
        rename_hash[rand_id] = rename_dict
        os.rename(src_path, dest_path)
        # if os.path.isfile(remove_path):
        #     os.remove(remove_path[:-1])
        # elif os.path.isdir(remove_path):
        #     os.rmdir(remove_path[:-1])
        client_socket.close()
        continue
    elif b"path" in data:
        delete_flag = 0
        # return to the client a random ID with digits, and lower\upper case letters.
        rand_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=128))
        print(rand_id + '\n')
        id_dict[rand_id] = 0  # false - didnt had change yet
        # To add a link
        # src_path = data[4:]
        client_socket.send(str(rand_id).encode())
        #########################################################
    elif b"first" in data:
        delete_flag = 0
        # data2 = client_socket.recv(1024)
        print("data2")
        print(data)
        # print(data2)
        rand_id = str(data)[7:-1]
        print(rand_id)
        # print(str(data)[3:-1])
        new_client = 1

        # client_socket.sendall(data)
        # data = client_socket.recv(100)
        # print(data)
        # print("rand")
        # print(rand_id)
    elif b'ENDID' in data:
        rand_id = str(data).split("ENDID")[0][2:]

    else:

        delete_flag = 0
        print("else")
        print(data.decode())
        rand_id = str(data)[2:-1]
        print("\n")
        #print("randid = " + rand_id)
        new_client = 0

    if delete_flag == 0:
        # Make a directory for the received files.
        os.makedirs(rand_id, exist_ok=True)
        with client_socket, client_socket.makefile('rb') as clientfile:
            while True:
                # Case we need to handle known client from different dir so we need to send him first all the files
                if new_client == 1:
                    print(rand_id)

                    with client_socket:

                        src_path = os.getcwd() + "\\" + rand_id
                        print(src_path)
                        # print(59)
                        # print(src_path)
                        for path, dirs, files in os.walk(src_path):
                            # print(path)
                            # print(dirs)
                            # print(files)
                            for file in files:
                                filename = os.path.join(path, file)
                                # print(filename)
                                relpath = os.path.relpath(filename, rand_id)
                                # print(relpath)
                                filesize = os.path.getsize(filename)
                                # print(filesize)
                                print(f'Sending {relpath}')
                                print("################")
                                print(relpath)
                                data_list.remove(relpath)
                                print(data_list)
                                print("################")
                                with open(filename, 'rb') as f:
                                    # print(i)
                                    # i += 1
                                    client_socket.sendall(relpath.encode() + b'\n')
                                    client_socket.sendall(str(filesize).encode() + b'\n')

                                    # Send the file in chunks so large files can be handled.
                                    while True:
                                        data = f.read(CHUNKSIZE)
                                        if not data:
                                            break
                                        # data_dec = data.decode()
                                        # data_list.remove(data_dec)
                                        # print("len")
                                        # print(len(data_list))
                                        # if len(data_list) == 0:
                                        #     client_socket.sendall("done".encode())
                                        #     print(88)
                                        #     break
                                        # if not data:
                                        #     client_socket.sendall("done".encode())
                                        #     break
                                        client_socket.sendall(data)
                                        # print(data.decode())

                        data_hash[rand_id] = data_list
                        print(data_hash[rand_id])
                        print("Done.")
                        client_socket.sendall("done".encode())
                        break
                #############################################################
                else:
                    raw = clientfile.readline()
                    if not raw:
                        client_socket.send(b'done')
                        client_socket.close()
                        break  # no more files, server closed connection.

                    filename = raw.strip().decode()
                    if "ENDID" in filename:
                        filename = filename.split("ENDID")[1]
                    length = int(clientfile.readline())
                    print(f'Downloading {filename}...\n  Expecting {length:,} bytes...', end='', flush=True)
                    if filename not in data_list:
                        data_list.append(filename)
                        data_hash[rand_id] = data_list
                    print("**************")
                    #print(data_hash[rand_id])
                    print("**************")
                    path = os.path.join(rand_id, filename)

                    #os.makedirs(os.path.dirname(path), exist_ok=True)
                    print("print")
                    print(path)
                    # Read the data in chunks so it can handle large files.
                    with open(path, 'wb') as f:
                        while length:
                            chunk = min(length, CHUNKSIZE)
                            data = clientfile.read(chunk)
                            if not data: break
                            f.write(data)
                            length -= len(data)
                        else:  # only runs if while doesn't break and length==0
                            print('Complete')
                            continue

                    # socket was closed early.
                    print('Incomplete')
                    # break

            ##########################################################################################

# class OnMyWatch:
#     # Set the directory on watch
#     watchDirectory = src_path
#
#     def __init__(self):
#         self.observer = Observer()
#
#     def run(self):
#         event_handler = Handler()
#         self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
#         self.observer.start()
#         try:
#             while True:
#                 # USE  THE CORRECT TIMER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#                 time.sleep(5)
#         except:
#             self.observer.stop()
#             print("Observer Stopped")
#
#         self.observer.join()
#
#
# class Handler(FileSystemEventHandler):
#
#     @staticmethod
#     def on_any_event(event):
#         if event.is_directory:
#             return None
#
#         elif event.event_type == 'created':
#             # Event is created, you can process it now
#             print("Watchdog received created event - % s." % event.src_path)
#         elif event.event_type == 'modified':
#             # Event is modified, you can process it now
#             print("Watchdog received modified event - % s." % event.src_path)
#
# while True:
#     watch = OnMyWatch()
#     watch.run()
#

# while True:
#     time.sleep(1)
# I think we should put it outside the while loop- because we do it only in the first time.
# client_socket, client_address = server.accept()
# data = client_socket.recv(100)
# if data[0] == "path":
#     # To add a link
#     src_path = data[1]
#     event_handler = Handler()
#     observer = watchdog.observers.Observer()
#     observer.schedule(event_handler, path=src_path, recursive=True)
#     observer.start()

# rand_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=128))
# client_socket.send(rand_id)
# while True:
#     client_socket, client_address = server.accept()
#     print('Connection from: ', client_address)
#     data = client_socket.recv(100)
#     print('Received: ', data)
#     client_socket.send(data.upper())
#     data = client_socket.recv(100)
#     print('Received: ', data)
#     client_socket.send(data.upper())
#     client_socket.close()
#    print('Client disconnected')
