import urllib.request
import urllib.parse
#DV Generator function
def digito_verificador(rut):
    value = 11 - sum([ int(a)*int(b)  for a,b in zip(str(rut).zfill(8), '32765432')])%11
    return {10: 'K', 11: '0'}.get(value, str(value))
def http_request(rut,key):
    try:
        url = 'https://zeus.sii.cl/cvc_cgi/stc/getstc'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
        dv = digito_verificador(rut)
        values = {'RUT' : rut,
                  'DV' : dv,
                  'txt_captcha' : key[1],
                  'txt_code' : key[0],
                  'PRG' : 'STC',
                  'OCP' : 'NOR',
                  'ACEPTAR' : '%C2%A0%C2%A0%C2%A0%C2%A0Consultar+situaci%C3%B3n+tributaria%C2%A0%C2%A0%C2%A0%C2%A0' }
        headers = { 'User-Agent' : user_agent,
                    'Cookie' : 'cert_Origin=directo',
                    'Referer' : 'https://zeus.sii.cl/cvc/stc/stc.html'
                    }
        data = urllib.parse.urlencode(values)
        data = data.encode()
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req)
        text = response.read().decode('latin-1')
        return text
    except:
        return 0