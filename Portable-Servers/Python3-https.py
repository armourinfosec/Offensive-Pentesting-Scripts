import socket
import os
import ssl
import argparse
from socketserver import BaseServer
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Default values
DEFAULT_CERT = 'cert.pem'
DEFAULT_KEY = 'key.pem'
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 443
DEFAULT_DIR = os.getcwd()

class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass, certfile, keyfile):
        BaseServer.__init__(self, server_address, HandlerClass)
        ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ctx.load_cert_chain(certfile=certfile, keyfile=keyfile)
        self.socket = ctx.wrap_socket(socket.socket(self.address_family, self.socket_type), server_side=True)
        self.server_bind()
        self.server_activate()

def main(HandlerClass=SimpleHTTPRequestHandler, ServerClass=SecureHTTPServer, certfile=DEFAULT_CERT, keyfile=DEFAULT_KEY, host=DEFAULT_HOST, port=DEFAULT_PORT, directory=DEFAULT_DIR):
    os.chdir(directory)
    server_address = (host, port) 
    httpd = ServerClass(server_address, HandlerClass, certfile, keyfile)
    sa = httpd.socket.getsockname()
    print(f"Serving HTTPS on {sa[0]} port {sa[1]} from {directory}...")
    httpd.serve_forever()

def parse_args():
    parser = argparse.ArgumentParser(description="Run a secure HTTPS server.")
    parser.add_argument('-c', '--cert', default=DEFAULT_CERT, help="Path to the SSL certificate (default: cert.pem)")
    parser.add_argument('-k', '--key', default=DEFAULT_KEY, help="Path to the SSL key (default: key.pem)")
    parser.add_argument('-H', '--host', default=DEFAULT_HOST, help="Host to bind to (default: '0.0.0.0')")
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT, help="Port to bind to (default: 443)")
    parser.add_argument('-d', '--directory', default=DEFAULT_DIR, help="Directory to serve (default: current directory)")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(certfile=args.cert, keyfile=args.key, host=args.host, port=args.port, directory=args.directory)
