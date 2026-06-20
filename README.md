# Snakenum

Snakenum is a small Python-based enumeration toolkit that provides a simple menu for running common recon tasks from one place.

Current modules include:

- **portsnake** — asynchronous TCP port scanner
- **dirsnake** — web directory and file brute-forcer

> Use Snakenum only on systems you own or have explicit permission to test.

## Features

- Interactive menu-driven interface
- Async TCP port scanning
- Optional start and end ports
- Web directory brute forcing with custom wordlists
- Configurable thread count for directory enumeration
- Simple modular design using importable Python files

## Requirements

- Python 3.10+
- `requests`

## Usage

Run the main menu:

```bash
python3 snakenum.py
```

Example menu:

```text
[+] Snake Enum Menu
[1] Port Scan
[2] Web Directory Brute Force
[0] Exit
[+] Select operation:
```

## Port Scanning

Choose option `1` from the menu.

You will be prompted for:

```text
[+] Target IP:
[+] Start port:
[+] End port:
```

If you leave the start and end ports blank, Snakenum should use the default range:

```text
1-65535
```

Example:

```text
[+] Target IP: 127.0.0.1
[+] Start port:
[+] End port:
```

This scans all ports on `127.0.0.1`.

## Directory Brute Forcing

Choose option `2` from the menu.

You will be prompted for:

```text
[+] Target URL:
[+] Wordlist:
[+] Threads:
```

Example:

```text
[+] Target URL: http://example.com
[+] Wordlist: /usr/share/wordlists/dirb/common.txt
[+] Threads: 20
```

The directory brute-forcer checks common paths and file extensions such as:

```text
.php
.bak
.orig
.inc
```

## Running Modules Directly

Each module can also be designed to run independently.

Example port scan:

```bash
python3 portsnake.py 127.0.0.1 1 1000
```

Example directory brute force:

```bash
python3 dirsnake.py -u http://example.com -w wordlist.txt -t 20
```

## Importing Modules

Snakenum is structured so individual modules can be imported and called from another Python file.

Example:

```python
import asyncio
import portsnake

asyncio.run(portsnake.main(["127.0.0.1", "1", "1000"]))
```

Example:

```python
import dirsnake

dirsnake.main([
    "-u", "http://example.com",
    "-w", "wordlist.txt",
    "-t", "20"
])
```

## Roadmap

Possible future improvements:

- Save scan results to a file
- Add JSON or CSV output
- Add timeout configuration
- Add HTTP status code filtering
- Add HTTPS support handling
- Add banner grabbing
- Add service detection
- Add rate limiting
- Add better error handling
- Add colored terminal output

## Disclaimer

This tool is intended for learning, lab work, and authorized security testing only. Do not use it against systems without permission.
