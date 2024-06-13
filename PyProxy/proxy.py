# Originally from http://sharebear.co.uk/blog/2009/09/17/very-simple-python-caching-proxy/
#
# Usage:
# A call to http://localhost:80000/example.com/foo.html will cache the file
# at http://example.com/foo.html on disc and not redownload it again. 
# To clear the cache simply do a `rm *.cached`. To stop the server simply
# send SIGINT (Ctrl-C). It does not handle any headers or post data. 

from http.server import BaseHTTPRequestHandler, HTTPServer
import hashlib
import os 
import urllib.request

class CacheHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        m = hashlib.md5()
        m.update(self.path.encode('utf-8'))
        cache_filename = m.hexdigest() + ".cached"
        if os.path.exists(cache_filename):
            print("Cache hit")
            with open(cache_filename, 'rb') as f:
                data = f.read()
        else:
            url = "http://proget.senstar-stellar.local" + self.path
            print("Cache miss -- trying: " + url)
            with urllib.request.urlopen(url) as response:
                data = response.read()
                with open(cache_filename, 'wb') as f:
                    f.write(data)

        # Calculate content length
        content_length = len(data)

        self.send_response(200)
        self.send_header('Content-Length', str(content_length))
        self.end_headers()
        self.wfile.write(data)

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CacheHandler)
    print('Starting server...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Server stopped.')

if __name__ == '__main__':
    run()