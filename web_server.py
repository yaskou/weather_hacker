import http.server
import socketserver

with socketserver.TCPServer(("",8000),http.server.SimpleHTTPRequestHandler) as httpd:
    print("Server Start\nServing at port=8000")
    httpd.serve_forever()