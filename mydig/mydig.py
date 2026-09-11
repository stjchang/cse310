import sys

ROOT_SERVERS = [
    "198.41.0.4"
]

def main():
    if len(sys.argv) != 2:
        print("Usage: python mydig.py <domain>")
        sys.exit(1)

    domain = sys.argv[1].rstrip(".")

    print(f"Resolving: {domain}")

    root_server = ROOT_SERVERS[0]

    print(f"Starting DNS server: {root_server}")


if __name__ == "__main__":
    main()