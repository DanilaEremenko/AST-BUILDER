import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import signal
import sys
import json


class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.command == 'GET' and self.path[0:7] == '/?year=':
            try:
                year = int(self.path[7:])
            except:
                self._send_all(1, "BAD YEAR NUMBER")
                return

            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                self._send_all(200, "12/09/%d" % year)
            else:
                self._send_all(200, "13/09/%d" % year)
        else:
            self._send_all(2, "BAD REQUEST")

    def _send_all(self, errorCode, dataMessage):
        self.send_response(200)
        self.send_header('content-type', 'text/json')
        self.end_headers()
        self.wfile.write(json.dumps({"errorCode": errorCode, "dataMessage": dataMessage}).encode())


def signal_handler(sig, frame):
    print('Exiting server')
    sys.exit(0)


def main():
    # parsing arguments
    parser = argparse.ArgumentParser(description="Simple http server with optional -p flag")
    parser.add_argument("-p", "--port", type=int, action="store", help="port")
    args = parser.parse_args()
    port = args.port if args.port is not None else 8080

    # running server
    print("Starting simple http server...")

    signal.signal(signal.SIGINT, signal_handler)
    print("SIGINT handler created")

    serv = HTTPServer(('', port), HttpProcessor)
    print("Requests expected on %d port\nRunning server..." % port)

    serv.serve_forever()


if __name__ == '__main__':
    main()
