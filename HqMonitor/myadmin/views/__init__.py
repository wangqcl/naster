from Crypto import Random
from Crypto.PublicKey import RSA


# 加密公私钥存储
def Encryption(request):
    RANDOM_GENERATOR = Random.new().read
    rsa = RSA.generate(1024, RANDOM_GENERATOR)
    #master的秘钥对的生成
    PRIVATE_PEM = rsa.exportKey()    # 公钥
    with open('myadmin/encryption/master-private.pem', 'w') as p:
        p.write(PRIVATE_PEM.decode())

    PUBLIC_PEM = rsa.publickey().exportKey()   # 私钥
    request.session['publickey'] = str(PUBLIC_PEM)

    with open('static/myadmin/master-public.pem', 'w') as f:
        f.write(PUBLIC_PEM.decode())
