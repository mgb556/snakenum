import asyncio
import argparse

async def scan_port(ip, port, timeout=1.0):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )

        writer.close()
        await writer.wait_closed()

        print(f"[+] Port {port} is OPEN")
        return port

    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None


async def main(argv=None):
    parser = argparse.ArgumentParser(description="Enumerate all open ports.")

    parser.add_argument("target_ip", help="Target IP")
    parser.add_argument("start_port", nargs="?", type=int, default=1, help="Start port")
    parser.add_argument("end_port", nargs="?", type=int, default=65535, help="End port")

    args = parser.parse_args(argv)

    target_ip = args.target_ip
    start_port = args.start_port
    end_port = args.end_port

    print(f"Starting async scan on {target_ip}...")

    tasks = [
        scan_port(target_ip, port)
        for port in range(start_port, end_port + 1)
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())