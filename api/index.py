import requests
import re

def handler(request):
    video_id = request.args.get("id")

    if not video_id:
        return {
            "statusCode": 200,
            "body": "Motor Online. Adicione ?id=xa0llxs no final da URL."
        }

    url_embed = f"https://www.dailymotion.com/embed/video/{video_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # 1. Headers de disfarce (Dizemos que somos o próprio Dailymotion)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.dailymotion.com/",
            "Origin": "https://www.dailymotion.com"
        }

        response = requests.get(url_embed, headers=headers).text
        # Busca o link .m3u8 no código da página
        match = re.search(r'"url":"(https://.*?\.m3u8.*?)"', response)

        if match:
            stream_url = match.group(1).replace("\\/", "/")
            
            return {
                "statusCode": 302,
                "headers": {
                    "Location": stream_url,
                    # LIBERA O ACESSO PARA O SMARTERS WEB
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Cache-Control": "no-cache, no-store, must-revalidate"
                }
            }
        else:
            return {
                "statusCode": 404,
                "body": "Stream não encontrado no código da página"
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": "Erro interno"
        }