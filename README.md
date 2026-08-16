# Client-Server Assignment

A multithreaded Python TCP application that supports concurrent terminal clients, server-status queries, file discovery, file retrieval, acknowledgements, and controlled disconnects.

The project demonstrates socket programming, thread-per-client concurrency, shared-state synchronization, command routing, and connection lifecycle tracking using only Python's standard library.

## Features

- TCP request/response communication on a configurable host and port
- A maximum of three concurrent clients
- One worker thread per accepted connection
- A lock-protected cache of client addresses and connection times
- Automatic creation of a shared `server_files/` repository
- Commands for status, file listing, file retrieval, and disconnecting

## Protocol commands

| Command | Server behavior |
| --- | --- |
| `status` | Returns known clients, addresses, and connection times |
| `list` | Lists files available in `server_files/` |
| `get <filename>` | Sends the requested file when it exists |
| `exit` | Closes the current client session |
| Any other text | Returns the message followed by `ACK` |

When three clients are active, additional connections receive `Server full. Try again later.` and are closed.

## Architecture

```text
Client.py                         Server.py
-----------                      -----------------------
terminal input  -- TCP socket -> accept loop
response print  <- TCP socket -- per-client worker thread
                                  |
                                  +-- shared client cache
                                  +-- server_files directory
                                  +-- command dispatcher
```

The server's accept loop assigns generated names such as `Client01`. Each connection is passed to a worker thread, while `clients_lock` protects updates to shared client state and the active-client counter.

## Run locally

### Prerequisites

- Python 3
- Two terminals on the same computer or local network

### Configure the host

Set `SERVER_HOST` in both `Server.py` and `Client.py` to the server machine's local IP address. For a same-computer test, use:

```python
SERVER_HOST = "127.0.0.1"
```

The default port is `12345`.

### Start the server

```bash
git clone https://github.com/HydraIsProgramming/Client-Server-Assignment.git
cd Client-Server-Assignment
python Server.py
```

The server creates `server_files/` automatically. Place files in that directory to make them available through the `list` and `get` commands.

### Connect clients

Open another terminal in the project directory:

```bash
python Client.py
```

Run additional client processes to test concurrent connections and the three-client limit.

## Project structure

| Path | Purpose |
| --- | --- |
| `Server.py` | TCP listener, worker threads, shared state, and command handling |
| `Client.py` | Interactive terminal client |
| `Server_Client Report.pdf` | Original design and project report |
| `LICENSE` | MIT licence |

## Engineering limitations

This is an educational local-network implementation, not an internet-facing file server. It does not include authentication, encryption, path sanitization, explicit message framing, chunk metadata, integrity checks, timeouts, or graceful server shutdown. Those controls would be required before accepting untrusted users or transferring arbitrary large files.

## License

This project is available under the [MIT License](LICENSE).
