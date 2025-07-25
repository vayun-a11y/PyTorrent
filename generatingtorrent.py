#SHA-1 (Secure Hash Algorithm 1) is a hash function.
#It turns any data (e.g., a 32 KB file chunk) into a 40-character hexadecimal string (160-bit hash). 
#Even a 1-bit change in data will produce a completely different hash

import os # lets you interact with files/folders (e.g. get file size).
import sys # read command line arguments
import hashlib #create sha1 hashes
import socket #to get your computer’s IP address.
import json #to save the .torrent file in readable format.

def sha1_pieces(filepath, piece_length=32 * 1024): #32 kb for sha1
    pieces = []
    with open(filepath, "rb") as f: #open a file(acc to a file path give) in binary mode(can interpret every thing as bytes even image)
        while True:#For each chunk, it creates a SHA-1 hash (unique fingerprint) and stores it in pieces.
            chunk = f.read(piece_length) #f.read(piece_length) automatically advances the file pointer to the next chunk.
            if not chunk:# If chunk is empty (end of file reached), exits the loop.
                break
            pieces.append(hashlib.sha1(chunk).hexdigest())#hashlib.sha1(chunk) creates a SHA-1 hash object. hashlib.sha1(chunk) creates a SHA-1 hash object
    return pieces

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        #  Connects to Google's DNS server (8.8.8.8) on port 80. This doesn't send data but reveals the local IP
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]# returns the local IP address
    finally:#Ensures the socket is closed even if errors occur.
        s.close()

def create_torrent(file_path):
    file_size = os.path.getsize(file_path)
    pieces = sha1_pieces(file_path) #calls the first fn that we defined
    torrent = {
        "name": os.path.basename(file_path),
        "length": file_size,
        "piece_length": 32 * 1024,
        "pieces": pieces,
        "peers": [{"ip": get_local_ip(), "port": 6881}]# 6881–6999 reseved for bit torrent traffic
    }

    out_name = os.path.basename(file_path) + ".torrent" #Sets the output filename (e.g., file.txt.torrent).
    with open(out_name, "w") as f:
        json.dump(torrent, f, indent=2)#Writes the torrent dictionary to a JSON file with 2-space indentation.

    print(f"Created torrent file: {out_name}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_torrent.py <file_path>")#generaste_torrent.py is first element and <file path is second elemrnt. if u didnt give these two it shows help message and exit
        sys.exit(1)

    file_path = sys.argv[1]#its index is one
    if not os.path.isfile(file_path):
        print(f"Error: '{file_path}' not found.")
        sys.exit(1)

    create_torrent(file_path)

if __name__ == "__main__":#Makes sure the main fn shld execute first
    main()