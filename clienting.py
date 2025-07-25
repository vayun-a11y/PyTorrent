import sys
import json
import socket

def recvall(sock, length):
    data = bytearray()
    while len(data) < length:#initiallu len is zero
        packet = sock.recv(length - len(data))#here sock ask for full size lets say 32kb.but it will give small part lets say 10kb.in next iteration length becomes 10kb and it asks for remaining 22kb.if it gives 12kb then in next iteration it ask remaining 10kb.likewise it run until they become equal.
        if not packet:
            raise EOFError("Connection closed before receiving all data")
        data.extend(packet)
    return data

def download_file(torrent_path):
    with open(torrent_path, "r") as f:
        torrent = json.load(f)

    ip   = torrent["peers"][0]["ip"]
    port = torrent["peers"][0]["port"]
    piece_length = torrent["piece_length"]
    total_length = torrent["length"]
    num_pieces   = len(torrent["pieces"])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    # Handshake
    sock.send(b"HELLO")
    sock.recv(1024)   # expect b"READY"

    file_data = bytearray()#Create empty buffer for downloaded data.dynamic buffer where we collect data as it comes in.

    for i in range(num_pieces):
        # Last piece may be smaller
        if i == num_pieces - 1:#For last piece → calculate actual remaining bytes
            expected = total_length - piece_length * (num_pieces - 1)
        else:# except the last → use piece_length (usually 32768)
            expected = piece_length

        sock.send(f"GET_PIECE_{i}".encode())
        chunk = recvall(sock, expected)
        file_data.extend(chunk)#Appends the piece to the final file_data buffer

    out_name = "downloaded_" + torrent["name"]
    with open(out_name, "wb") as f:
        f.write(file_data)

    sock.close()
    print(f"Download complete: {out_name}")
    print(f"Original size: {total_length} bytes")
    print(f"Downloaded size: {len(file_data)} bytes")

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <torrent_file>")
        sys.exit(1)

    download_file(sys.argv[1])

if __name__ == "__main__":
    main()