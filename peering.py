import sys
import json
import socket

def handle_client(conn, torrent, file_path):
    # Handshake
    conn.recv(1024)         # expect b"HELLO" can receive upto 1024 bytes
    conn.send(b"READY")     # acknowledge

    piece_length = torrent["piece_length"] #32kb
    num_pieces = len(torrent["pieces"])

    with open(file_path, "rb") as f:#Opens the actual file to send 
        for i in range(num_pieces):
            req = conn.recv(1024).decode()#.decode() converts bytes → string (e.g., b'GET_PIECE_1' → 'GET_PIECE_1')
            if req == f"GET_PIECE_{i}":#created by client
                f.seek(i * piece_length) #f.seek(n) moves the read/write position to the nth byte it is necessary becauseWaiting for the client to request a specific piece And then jumping to the exact byte position where that piece begins
                data = f.read(piece_length)
                conn.send(data)

    conn.close()

def start_seeder(torrent_path, file_path):
    with open(torrent_path, "r") as f:
        torrent = json.load(f) #Parses the JSON content from the file and loads it into a Python dictionary i.e., torrent.

    port = torrent["peers"][0]["port"]#we are using only one peer.0 is not needed so dont confuse
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creating tcp server.SOCK_STREAM means TCP
    server.bind(("", port))#binds to specied port ."" means "listen on all local IP addresses".
    server.listen(1)#starts listening for one connection at a time
    print(f"Seeding '{file_path}' on port {port}…")

    while True:
        conn, _ = server.accept() #conn is a new socket used to talk to tht one client
        handle_client(conn, torrent, file_path)

def main():
    if len(sys.argv) != 3:
        print("Usage: python real_peer.py <torrent_file> <data_file>")
        sys.exit(1)

    torrent_file = sys.argv[1]
    data_file = sys.argv[2]
    start_seeder(torrent_file, data_file)

if __name__ == "__main__":
    main()