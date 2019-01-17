import hashlib, binascii
from Crypto.Cipher import AES # pip install pycrypto

# md5 hashing same input give same output
md5_str1 = hashlib.new("md5", "HELLO").hexdigest()
print md5_str1
md5_str2 = hashlib.new("md5", "HELLO").hexdigest()
print md5_str2

# Naive algorithms such as sha1(password) are not resistant against brute-force
# attacks. A good password hashing function must be tunable, slow, and include
# a salt.
sha_result1 = hashlib.pbkdf2_hmac('sha256', b'HELLO', b'salt', 100000)
sha_str1 = binascii.hexlify(sha_result1)
print sha_str1
# same input, same salt, same output
sha_result2 = hashlib.pbkdf2_hmac('sha256', b'HELLO', b'salt', 100000)
sha_str2 = binascii.hexlify(sha_result2)
print sha_str2
# same input, different salt, different output
sha_result3 = hashlib.pbkdf2_hmac('sha256', b'HELLO', b'vinegar', 100000)
sha_str3 = binascii.hexlify(sha_result3)
print sha_str3

# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 20
# the size multiple required for AES
AES_MULTIPLE = 16

def generate_key(password, salt, iterations):
    assert iterations > 0

    key = password + salt

    for i in range(iterations):
        key = hashlib.sha256(key).digest()  

    return key

def pad_text(text, multiple):
    extra_bytes = len(text) % multiple

    padding_size = multiple - extra_bytes

    padding = chr(padding_size) * padding_size

    padded_text = text + padding

    return padded_text

def unpad_text(padded_text):
    padding_size = ord(padded_text[-1])

    text = padded_text[:-padding_size]

    return text

def encrypt(plaintext, password):
    salt = 'seasalt' #Crypto.Random.get_random_bytes(SALT_SIZE)

    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)

    cipher = AES.new(key, AES.MODE_ECB)

    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)

    ciphertext = cipher.encrypt(padded_plaintext)

    ciphertext_with_salt = salt + ciphertext

    return ciphertext_with_salt

def decrypt(ciphertext, password):
    salt = 'seasalt' #ciphertext[0:SALT_SIZE]

    ciphertext_sans_salt = ciphertext[SALT_SIZE:]

    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)

    cipher = AES.new(key, AES.MODE_ECB)

    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)

    plaintext = unpad_text(padded_plaintext)

    return plaintext

#enc_str = encrypt('TO DEBUG IS', 'superhuman')
#dec_str = decrypt(enc_str, 'superhuman')
#print dec_str






