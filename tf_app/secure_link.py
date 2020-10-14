from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_text,force_bytes
import hashlib
import time

expire_time=''


def encode(email,user_time):
    global expire_time
    expire_time = 1000
    user=User.objects.get(email=email)
    token = str(user_time)+user.username+email+str(user.pk)
    token = hashlib.sha1(token.encode()).hexdigest()
    main_token = urlsafe_base64_encode(force_bytes(str(user.pk)+','+str(time.time())+','+token))
    return main_token

def decode(receive_token,verify,main):
    try:
        global expire_time
        main_token = urlsafe_base64_decode(force_text(receive_token)).decode('utf-8')
        main_token = main_token.split(',')
        print(expire_time,'before post request')
        if(int(float(main_token[1]))>=int(float(time.time()))-expire_time):
            if main:
                if expire_time>0:
                    user = User.objects.get(pk=main_token[0])
                    return user
            user = User.objects.get(pk=main_token[0])
            expire_time=0
            print(expire_time,'after post request')
            if verify=='password':
                joined_login_time = user.last_login
            elif verify=='register':
                joined_login_time = user.date_joined
            user_token = str(joined_login_time)+user.username+user.email+str(user.pk)
            user_token = hashlib.sha1(user_token.encode()).hexdigest()
            print(main_token[2])
            print(user_token)
            if user_token == main_token[2]:
                return user
        return 'invalid'
    except:
        return 'invalid'

    

