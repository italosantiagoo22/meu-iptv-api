import requests
import re
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Pega o ID da URL
        query = parse_qs(urlparse(self.path).query)
        video_id = query.get('id', [None])[0]

        if not video_id:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Motor Online. Adicione ?id=xa0llxs no final da URL.")
            return

        # Busca o token no Dailymotion
        url_embed = f"https://www.dailymotion.com/embed/video/{video_id}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            response = requests.get(url_embed, headers=headers).text
            match = re.search(r'"url":"(https://.*?\.m3u8.*?)"', response)
            
            if match:
                stream_url = match.group(1).replace("\\/", "/")
                # REDIRECIONA PARA O VÍDEO REAL
                self.send_response(302)
                self.send_header('Location', stream_url)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        except:
            self.send_response(500)
            self.end_headers()