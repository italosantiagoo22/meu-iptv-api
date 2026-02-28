from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import re

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Pega o ID que você enviou na URL (?id=xxxxxx)
        query = parse_qs(urlparse(self.path).query)
        video_id = query.get('id', [None])[0]

        if not video_id:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Erro: ID do video nao fornecido.")
            return

        url_video = f"https://www.dailymotion.com/embed/video/{video_id}"
        
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url_video, headers=headers).text
            
            # Busca o link do manifesto (m3u8) com o token atualizado
            match = re.search(r'"url":"(https://.*?\.m3u8.*?)"', response)
            
            if match:
                stream_url = match.group(1).replace("\\/", "/")
                
                # Redireciona a TV para o link real com o token de agora
                self.send_response(302)
                self.send_header('Location', stream_url)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
                
        except Exception:
            self.send_response(500)
            self.end_headers()