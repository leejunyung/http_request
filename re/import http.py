import http.server
import socketserver
import os
import cgi

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_type = self.headers.get('Content-Type')
        boundary = content_type.split("=")[1].encode()
        remainbytes = int(self.headers['Content-Length'])
        line = self.rfile.readline()
        remainbytes -= len(line)

        if boundary not in line:
            self.send_error(400, "Content not begin with boundary")
            return

        line = self.rfile.readline()
        remainbytes -= len(line)
        
        disposition_header, disposition_params = cgi.parse_header(line.decode())
        fn = disposition_params.get('filename', 'uploaded_file')

        path = os.path.join("uploads", fn)
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        
        with open(path, 'wb') as out:
            preline = self.rfile.readline()
            remainbytes -= len(preline)
            while remainbytes > 0:
                line = self.rfile.readline()
                remainbytes -= len(line)
                if boundary in line:
                    preline = preline[0:-1]
                    out.write(preline)
                    break
                else:
                    out.write(preline)
                    preline = line

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'File uploaded successfully')

if __name__ == "__main__":
    PORT = 8000
    Handler = SimpleHTTPRequestHandler
    with socketserver.TCPServer(('127.0.0.1', PORT), Handler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
