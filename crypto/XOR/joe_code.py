from PIL import Image
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.number import bytes_to_long as b2l

def img_to_pixels(path="qr_code.png") -> list[int]:
    qr_code = Image.open(path)
    size = qr_code.size
    pixels = []
    for i in range(size[0]):
        for j in range(size[1]):
            pixels.append(sum(qr_code.getpixel((i,j))[:3])//3)
    assert len(pixels) == 31*31
    return pixels

def joe_AES_CTR(buffer: list[int], key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    counter = get_random_bytes(16)
    for n in range(len(buffer)):
        if n%16 == 0:
            counter = (b2l(counter) + 1).to_bytes(16)
            aes_ctr = cipher.encrypt(counter)
        buffer[n] = buffer[n] ^ int(counter[n%16])

pixels = img_to_pixels()
joe_AES_CTR(pixels, get_random_bytes(16))
with open("encrypted_qr_code", "+wb") as encrypted_file:
    encrypted_file.write(bytes(pixels))
