# RSA encryption
from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import hashlib
import json

rcv = {
    'mode': 'logined'
}
msg = json.dumps(rcv)

random_generator = Random.new().read
key = RSA.generate(1024, random_generator) #generate pub and priv key
publickey = key.publickey().exportKey() # pub key export for exchange
privatekey = key.exportKey()
hashobj = hashlib.sha1(publickey)
hashdigest = hashobj.hexdigest()
# encrypt
encryption = PKCS1_OAEP.new(key)
emsg_1 = encryption.encrypt(msg.encode())
emsg_2 = emsg_1.hex().upper()
# decrypt
nmsg = bytes.fromhex(emsg_2).lower()
decryption = PKCS1_OAEP.new(key)
dmsg = decryption.decrypt(nmsg)

