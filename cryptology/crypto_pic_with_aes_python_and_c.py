import time
from Crypto.Cipher import AES
import numpy as np
import cv2
import c_mod

# c version pic_map
c_mod.init_func()

pic_map = {}
alt_map = ["a" for i in range(256)]
char_map = "abcdefghijklmnopqrstuvwxyz"

count = 0
for i in range(16):
    for j in range(16):
        s = char_map[i] + char_map[j]
        pic_map[s] = count
        alt_map[count] = s
        count += 1


def str2img(ss, shape, pic_map):
    m, n, c = shape
    pic_tmp = np.zeros((m, n, c))
    count = 0
    for k in range(c):
        for j in range(n):
            for i in range(m):
                s = ss[count:count+2]
                count += 2
                pic_tmp[i, j, k] = pic_map[s]
    return pic_tmp


def img2str(img, shape):
    ss = u''
    m, n, c = shape
    img = img.reshape((m*n*c))
    for i in range(m*n*c):
        ss = ss + alt_map[img[i]]

    return ss


img = cv2.imread("./rgb.png")
img = cv2.pyrUp(img)
img = np.array(img)
shape = img.shape

pic = np.zeros((shape[0]*shape[1]*shape[2]))

key = "This is a key123"
iv = "This is an IV456"
encoder = AES.new(bytes(key, encoding="utf-8"), AES.MODE_CBC, bytes(iv, encoding="utf-8"))
decoder = AES.new(bytes(key, encoding="utf-8"), AES.MODE_CBC, bytes(iv, encoding="utf-8"))
content = img2str(img, shape)
print(content[0:10])
content = bytes(content, encoding="utf-8")

print("开始加密")
s1 = time.time()
ciphertext = encoder.encrypt(content)
e1 = time.time()
print("加密结束", e1 - s1)

print("-"*30+"分割线"+"-"*30)

print("开始解密")
s2 = time.time()
decoded = decoder.decrypt(ciphertext)
e2 = time.time()
print(bytes.decode(decoded)[0:10])
print("解密结束", e2 - s2)

s3 = time.time()
c_mod.c_str2numpy_func(bytes.decode(decoded), pic)
pic = np.reshape(pic, shape)/255
cv2.imshow("decoded", pic)
e3 = time.time()
print("图像解码耗时", e3 - s2)
cv2.waitKey()

