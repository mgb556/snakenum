import asyncio
from modules import dirsnake, portsnake


def menu():
    print("[+] Snake Enum Menu")
    print("[1] Port Scan")
    print("[2] Web Directory Brute Force")
    print("[0] Exit")

    selection = input("[+] Select operation: ")

    match selection:
        case "1":
            target = input("[+] Target IP: ").strip()
            start_port = input("[+] Start port: ").strip()
            end_port = input("[+] End port: ").strip()

            argv = [target]

            if start_port and end_port:
                argv.extend([start_port, end_port])
            elif start_port:
                argv.append(start_port)
            elif end_port:
                argv.extend(["1", end_port])

            asyncio.run(portsnake.main(argv))

        case "2":
            url = input("[+] Target URL: ").strip()
            wordlist = input("[+] Wordlist: ").strip()
            threads = input("[+] Threads: ").strip()

            argv = ["-u", url, "-w", wordlist]

            if threads:
                argv.extend(["-t", threads])

            dirsnake.main(argv)

        case "0":
            print("[+] Exiting")

        case _:
            print("[-] Invalid selection")


if __name__ == "__main__":
    menu()