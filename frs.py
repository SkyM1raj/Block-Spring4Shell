# www.theforage.com - Telstra Cyber Task 3
# Firewall Server Handler

from http.server import BaseHTTPRequestHandler, HTTPServer
import re

host = "localhost"
port = 8000

class ServerHandler(BaseHTTPRequestHandler):

    def block_request(self):
        self.send_response(403)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"error": "Forbidden Access"}')
        print("Blocking request")

        def rule_1(): #Blocking payload
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""

            if re.search(r'class\.module\.classLoader\.resources\.context\.parent\.pipeline\.first', post_data):
                self.block_request()
                return True
            return False

        def rule_2(): #Blocking headers
            if (self.headers.get("suffix") == "%>//" and
                self.headers.get("C1") == "Runtime" and
                self.headers.get("C2") == "<%" and
                self.headers.get("DNT") == "1" and
                self.headers.get("Content-Type") == "application/x-www-form-urlencoded"):
                self.block_request()  # Bloque la requête si les critères sont remplis
                return True
            return False

        if rule_1() or rule_2():#Conditions
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"message": "Request received"}')

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

if __name__ == "__main__":
    server = HTTPServer((host, port), ServerHandler)
    print("[+] Firewall Server")
    print("[+] HTTP Web Server running on: %s:%s" % (host, port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("[+] Server terminated. Exiting...")
    exit(0)