import argparse
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Simple FTP Server using pyftpdlib")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="IP address to bind the FTP server (default: 0.0.0.0)")
    parser.add_argument("-P", "--port", type=int, default=21, help="Port number for the FTP server (default: 21)")
    parser.add_argument("-u", "--user", type=str, help="Username for the FTP server (optional)")
    parser.add_argument("-p", "--password", type=str, help="Password for the FTP server user (optional)")
    parser.add_argument("-d", "--directory", type=str, default="/tmp", help="Directory to share via FTP (default: /tmp)")
    parser.add_argument("--disable-anonymous", action="store_true", help="Disable anonymous access to the FTP server")

    args = parser.parse_args()

    # Set up authorizer
    authorizer = DummyAuthorizer()

    if args.user and args.password:
        authorizer.add_user(args.user, args.password, args.directory, perm="elradfmw")
        print(f"User mode: Username - {args.user}, Password - {args.password}")
    elif not args.disable_anonymous:
        authorizer.add_anonymous(args.directory, perm="elradfmw")
        print("Anonymous mode enabled by default.")
    else:
        print("Anonymous access is disabled.")

    # Set up FTP handler
    handler = FTPHandler
    handler.authorizer = authorizer

    # Start FTP server
    server = FTPServer((args.host, args.port), handler)
    print(f"Starting FTP server on {args.host}:{args.port}")
    print(f"Shared directory: {args.directory}")
    server.serve_forever()

if __name__ == "__main__":
    main()
