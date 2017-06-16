import hmac
from hashlib import sha1
import time
import base64

key = base64.b64decode("0w7E2kD+8d2Sn05ebNXmxONwE3DtcVBPo+0JxrBr3yc=")
token_lifetime = 1209600 # 2 weeks

path = "/foo/bar.html"
entitlement = "UserReadUS"
expiration = int(time.time()) + token_lifetime

string_to_sign = "{0}{1}".format(path,expiration)
#print (string_to_sign)

digest = hmac.new(key, string_to_sign.encode('utf-8'), sha1)

signature = digest.hexdigest()

token = "{0}_{1}_{2}".format(expiration, signature, entitlement)

print ("Token:   " + token)
#print ("decoded: " + token)