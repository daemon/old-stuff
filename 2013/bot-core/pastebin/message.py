import urllib.parse as parse
import urllib.request

class PastebinRequestFactory:
    def __init__(self, dev_key, api_paste_code):
        self.params = {'api_dev_key':dev_key, 'api_paste_code':api_paste_code,
                       'api_option':'paste'}

    def paste_name(self, name):
        self.params['api_paste_name'] = name
        return self

    def user_name(self, name):
        self.params['api_user_name'] = name
        return self

    def password(self, pw):
        self.params['api_user_password'] = pw

    def user_key(self, userkey):
        self.params['api_user_key'] = userkey
        return self

    def paste_format(self, p_format):
        self.params['api_paste_format'] = p_format
        return self

    def paste_private(self, p_id):
        self.params['api_paste_private'] = p_id
        return self

    def paste_expire_date(self, expire_date):
        self.params['api_paste_expire_date'] = expire_date
        return self

    def makeRequest(self):
        try:
            name = self.params['api_user_name']
            password = self.params['api_user_password']
            content = urllib.request.urlopen('http://pastebin.com/api/api_login.php', parse.urlencode(self.params).encode('utf-8')).read().decode('utf-8', 'ignore')
            self.params['api_user_key'] = content
            print(content)
        except KeyError:
            pass
        return PastebinRequest(parse.urlencode(self.params))

class PastebinRequest:
    api_url = "http://pastebin.com/api/api_post.php"
    def __init__(self, request):
        self.request = request

    def doRequest(self):
        return urllib.request.urlopen(self.api_url, self.request.encode('utf-8'))
