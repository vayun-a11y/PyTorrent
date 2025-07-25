# SimplePyTorrent: A Minimalist BitTorrent Implementation in Python

##  Overview

SimplePyTorrent is a basic, educational implementation of the BitTorrent protocol using Python. This project demonstrates the fundamental concepts of peer-to-peer file sharing, including torrent file generation, file seeding (serving files), and file downloading (client functionality). It's designed to be straightforward and easy to understand, making it an excellent starting point for anyone interested in how BitTorrent works under the hood.

##  Features

* **Torrent File Generation (`generatingtorrent.py`):**
    * Creates `.torrent` files for any given file.
    * Calculates SHA-1 hashes for file chunks (pieces) to ensure data integrity.
    * Includes metadata like file name, size, piece length, and peer information (local IP for a simple setup).
* **File Seeding (`peering.py`):**
    * Acts as a "seeder" (peer) that serves file pieces to clients.
    * Listens for incoming connections and responds to piece requests.
    * Implements a basic handshake mechanism.
* **File Downloading (`clienting.py`):**
    * Functions as a "leecher" (client) to download files from a seeder using a `.torrent` file.
    * Requests file pieces sequentially.
    * Includes a `recvall` helper to ensure complete reception of data chunks.
    * Saves the downloaded file to disk.

##  How it Works (Simplified)

1.  **Generate a Torrent:** You start by running `generatingtorrent.py` on the file you want to share. This creates a `.torrent` file containing metadata about the file and its pieces.
2.  **Start Seeding:** The `.torrent` file is then used by `peering.py` (the seeder). The seeder opens the original file and listens for incoming connections from clients on a specified port.
3.  **Client Downloads:** A client runs `clienting.py` with the `.torrent` file. It connects to the seeder, performs a simple handshake, and then requests file pieces one by one.
4.  **Piece by Piece:** The seeder reads the requested piece from the original file and sends it to the client. The client receives and reassembles these pieces until the entire file is downloaded.
5.  **Data Integrity:** SHA-1 hashes (though not verified in the current client implementation for simplicity) are included in the torrent file to conceptually allow for checking if downloaded pieces are corrupted or tampered with.

## 🛠️ Setup and Usage

### Prerequisites

* Python 3.x installed on your system.

### Installation

No special installation steps required. Simply clone the repository

