# -*- coding: utf-8 -*-
import random,string,hashlib,base64
import time
import hmac

class UserService():

    @staticmethod
    def geneAuthCode( user_info = None ):
        m = hashlib.md5()
        str = "%s-%s-%s-%s-%s"%( user_info.id,user_info.login_name,user_info.login_pwd,
                                 user_info.login_salt,user_info.status )
        m.update( str.encode("utf-8") )
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd,salt):
        m = hashlib.md5()
        str = "%s-%s"%( base64.encodebytes( pwd.encode("utf-8") ),salt  )
        m.update( str.encode("utf-8") )
        return m.hexdigest()

    @staticmethod
    def geneSalt( length = 16 ):
       keylist  = [ random.choice( (string.ascii_letters + string.digits ) ) for i in range(length ) ]
       return ( "".join( keylist) )
    
    # token加密版本2 
    @staticmethod
    def generate_token(key, expire=3600):
        """
        :param key:  str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
        :param expire: int(最大有效时间，单位为s)
        :return:  state: str
        """
        ts_str = str(time.time() + expire)
        ts_byte = ts_str.encode("utf-8")
        sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
        token = ts_str + ':' + sha1_tshexstr
        b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
        return b64_token.decode("utf-8")

    @staticmethod
    def certify_token(key, token):
        """
        :param key: str
        :param token: str
        :return:  boolean
        """
        token_str = base64.urlsafe_b64decode(token).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 2:
            return False
        ts_str = token_list[0]
        if float(ts_str) < time.time():
            # token expired
            return False
        known_sha1_tsstr = token_list[1]
        sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
        calc_sha1_tsstr = sha1.hexdigest()
        if calc_sha1_tsstr != known_sha1_tsstr:
            # token certification failed
            return False
            # token certification success
        return True
    