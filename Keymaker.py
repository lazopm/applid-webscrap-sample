import urllib.request
import urllib.parse
import json
import base64
import time
def generate():
    for _ in range(40):
        try:
            url = 'https://zeus.sii.cl/cvc_cgi/stc/CViewCaptcha.cgi'
            values = {'oper':0}
            data = urllib.parse.urlencode(values).encode('latin-1')
            response = urllib.request.urlopen(url, data)
            text = response.read().decode('latin-1')
            arr = json.loads(text)
            return [base64.b64decode(arr['txtCaptcha']).decode('latin-1')[36:40],arr['txtCaptcha']]
        except:
            time.sleep(.5)
            pass