from lxml import etree
import requests
# import pdb

class Login():
    """
    登录类,为实例提供了初始化状态和方法
    """
    
    def __init__(self):
        """
        初始化请求头,跳转url信息,会话
        """
        
        self.headers = {
            'Referer': 'https://github.com/',
            'Host': 'github.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/68.0.3440.75 Chrome/68.0.3440.75 Safari/537.36'
            }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()

    def token(self):
        """
        获取authticity_token信息(一个隐藏的input),为伪造表单登录提供信息
        """
        
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//form/input[2]/@value')[0]
        return token

    def login(self, email, password):
        """
        伪造表单登录
        """
        
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token':self.token(),
            'login': email,
            'password': password
            }
        response = self.session.post(self.post_url, data=post_data,headers=self.headers)
        #if response.status_code == 200:
        #    self.dynamics(response.text)
        response = self.session.get(self.logined_url,headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)

    def dynamics(self, html): # 得不到,渲染后才出来的数据
        selector = etree.HTML(html)
        dynamics =selector.xpath('//a[@data-hovercard-user-id]')
        for item in dynamics:
            dynamic = item.xpath('./parent/text()')
            print(dynamic)

    def profile(self, html):
        """
        到个人信息页,获取个人信息
        """
        
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name, email)


if __name__ == '__main__':
    # pdb.set_trace()
    login = Login()
    login.login(email='email', password='password')
