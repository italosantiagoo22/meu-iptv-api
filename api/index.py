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
        response = requests.get(url_embed, headers=headers).text
        match = re.search(r'"url":"(https://.*?\.m3u8.*?)"', response)

        if match:
            stream_url = match.group(1).replace("\\/", "/")
            return {
                "statusCode": 302,
                "headers": {
                    "Location": stream_url
                }
            }
        else:
            return {
                "statusCode": 404,
                "body": "Stream não encontrado"
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": "Erro interno"
        }