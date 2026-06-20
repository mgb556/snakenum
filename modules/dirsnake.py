import argparse
import queue
import requests
import sys
import threading


AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
EXTENSIONS = [".php", ".bak", ".orig", ".inc"]


def get_words(wordlist, resume=None):
    words = queue.Queue()

    def extend_words(word):
        if "." in word:
            words.put(f"/{word}")
        else:
            words.put(f"/{word}/")

        for extension in EXTENSIONS:
            words.put(f"/{word}{extension}")

    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        raw_words = f.read()

    found_resume = resume is None

    for word in raw_words.split():
        if not found_resume:
            if word == resume:
                found_resume = True
                print(f"Resuming wordlist from: {resume}")
            continue

        extend_words(word)

    return words


def dir_bruter(target, words):
    headers = {"User-Agent": AGENT}

    while True:
        try:
            path = words.get_nowait()
        except queue.Empty:
            return

        url = f"{target.rstrip('/')}{path}"

        try:
            r = requests.get(url, headers=headers, timeout=5)
        except requests.exceptions.ConnectionError:
            sys.stderr.write("x")
            sys.stderr.flush()
            continue
        except requests.exceptions.Timeout:
            sys.stderr.write("t")
            sys.stderr.flush()
            continue

        if r.status_code == 200:
            print(f"\nSuccess ({r.status_code}): {url}")
        elif r.status_code == 404:
            sys.stderr.write("../..")
            sys.stderr.flush()
        else:
            print(f"\n{r.status_code} => {url}")


def run(url, wordlist, threads=10, resume=None, wait_for_enter=False):
    words = get_words(wordlist, resume=resume)

    if wait_for_enter:
        print("Press return to continue")
        sys.stdin.readline()

    thread_list = []

    for _ in range(threads):
        t = threading.Thread(target=dir_bruter, args=(url, words))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()


def build_parser():
    parser = argparse.ArgumentParser(description="Brute force web directories and files")

    parser.add_argument("-u", "--url", required=True, type=str, help="Target URL")
    parser.add_argument("-w", "--wordlist", required=True, type=str, help="Wordlist file")
    parser.add_argument("-t", "--threads", default=10, type=int, help="Number of threads")
    parser.add_argument("-r", "--resume", default=None, type=str, help="Resume from this word")
    parser.add_argument("--pause", action="store_true", help="Wait for Enter before starting")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    run(
        url=args.url,
        wordlist=args.wordlist,
        threads=args.threads,
        resume=args.resume,
        wait_for_enter=args.pause,
    )


if __name__ == "__main__":
    main()