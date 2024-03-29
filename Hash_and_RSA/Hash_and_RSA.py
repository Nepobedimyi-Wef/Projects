import hashlib
import rsa
(pub_key,privat_key) = rsa.newkeys(1024)
pub_key,privat_key = privat_key,pub_key
def hash(hash_text):
    hash_object = hashlib.sha256()
    hash_object.update(hash_text.encode())
    hashed_text = hash_object.hexdigest()
    return hashed_text
hash_string = input("Введите открытый текст: ")
hashed = hash(hash_string)
msg = hashed
encrypted = rsa.encrypt(msg.encode(), privat_key)
hash_string1 = input("Введите текст: ")
hashed1 = hash(hash_string1)
unencrypted = rsa.decrypt(encrypted, pub_key)
if unencrypted.decode() == hashed1:
    print("ЭП верна")
else:
    print("ЭП неверна")
