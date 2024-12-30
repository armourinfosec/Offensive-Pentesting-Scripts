import BaseHTTPServer
import SimpleHTTPServer
import ssl
import argparse
import os

# Default values
DEFAULT_CERT = 'cert.pem'
DEFAULT_KEY = 'key.pem'
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 443
DEFAULT_DIR = os.getcwd() 

class SecureHTTPServer(BaseHTTPServer.HTTPServer):
    def __init__(self, server_address, HandlerClass, certfile, keyfile):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, HandlerClass)
        self.socket = ssl.wrap_socket(self.socket, keyfile=keyfile, certfile=certfile, server_side=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Run a secure HTTPS server.")
    parser.add_argument('-c', '--cert', default=DEFAULT_CERT, help="Path to the SSL certificate (default: cert.pem)")
    parser.add_argument('-k', '--key', default=DEFAULT_KEY, help="Path to the SSL key (default: key.pem)")
    parser.add_argument('-H', '--host', default=DEFAULT_HOST, help="Host to bind to (default: '0.0.0.0')")
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT, help="Port to bind to (default: 443)")
    parser.add_argument('-d', '--directory', default=DEFAULT_DIR, help="Directory to serve (default: current directory)")
    return parser.parse_args()

def main(HandlerClass=SimpleHTTPServer.SimpleHTTPRequestHandler, ServerClass=SecureHTTPServer, certfile=DEFAULT_CERT, keyfile=DEFAULT_KEY, host=DEFAULT_HOST, port=DEFAULT_PORT, directory=DEFAULT_DIR):
    os.chdir(directory)  
    server_address = (host, port)
    httpd = ServerClass(server_address, HandlerClass, certfile, keyfile)
    print("Serving HTTPS on %s port %d from %s..." % (host, port, directory))
    httpd.serve_forever()

if __name__ == '__main__':
    args = parse_args()
    main(certfile=args.cert, keyfile=args.key, host=args.host, port=args.port, directory=args.directory)