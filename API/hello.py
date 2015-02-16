import urllib.parse as upar
import urllib.request as ureq
import io
import gzip

url = 'http://myanimelist.net/api/anime/search.xml?q=neon'
url2 = 'http://myanimelist.net/api/account/verify_credentials.xml'
url3 = 'http://myanimelist.net/api/animelist/update/30.xml'
url4 = 'http://myanimelist.net/includes/ajax.inc.php?id=22419&t=64'

headers = {
			'Host': 'myanimelist.net',
			'Accept': 'text/xml, text/*',
			'Accept-Charset': 'utf-8',
			'Accept-Encoding': 'gzip',
			'Authorization': 'Basic cXVldHphbGNvYXRsMzg0OnBhc3N3b3Jk',
			'User-Agent': 'api-taiga-32864c09ef538453b4d8110734ee355b'
		}
		
values = {
			'data': '<?xml version="1.0" encoding="UTF-8"?><entry><score>10</score></entry>'
		}

data = upar.urlencode(values).encode('utf-8')
bs = ureq.urlopen(ureq.Request(url4, None, headers)).read()
bi = io.BytesIO(bs)
gf = gzip.GzipFile(fileobj=bi, mode='rb')
print(gf.read())