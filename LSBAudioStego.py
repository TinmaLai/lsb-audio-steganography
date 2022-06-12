import os.path
import wave
import unicodedata
import numpy as np
import cv2
from PIL import Image

from AudioStegnographyAlgorithm import AudioStego

# Mã hóa LSB thông qua video
class LSBAudioStego(AudioStego):
    # Hàm xuất file output
    def saveToLocation(self, audioArray, location):
        # Tạo ra một file mới để chứa output, tên là output-lsb.wav
        dir = os.path.dirname(location)
        self.newAudio = wave.open(dir + "/output-lsb.wav", 'wb')
        self.newAudio.setparams(self.audio.getparams())
        self.newAudio.writeframes(audioArray)
        self.newAudio.close()
        self.audio.close()
        return dir + "/output-lsb.wav"
    def saveToLocation2(self, audioArray, location):
        # Tạo ra một file mới để chứa output, tên là output-lsb.wav
        dir = os.path.dirname(location)
        self.newAudio = wave.open(dir + "/output-image-lsb.wav", 'wb')
        self.newAudio.setparams(self.audio.getparams())
        self.newAudio.writeframes(audioArray)
        self.newAudio.close()
        self.audio.close()
        return dir + "/output-image-lsb.wav"
    # Hàm mã hóa audio
    def encodeAudio(self, audioLocation, stringToEncode, ) -> str:
        # Băm đoạn âm thanh thành 1 mảng các byteS
        audioArray = self.convertToByteArray(audioLocation)
        # stringToEncode = stringToEncode.encode('utf-8')
        # stringToEncode = str(stringToEncode) + '\n'
        # Chuyển chuỗi thông điệp sang array
        stringToEncode = stringToEncode + int((len(audioArray) - (len(stringToEncode) * 8 * 8)) / 13) * '#'
        # print(stringToEncode)
        # bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in stringToEncode])))
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(13, '0') for i in stringToEncode])))
        # print(bits)
        # Thực hiện LSB, vói từng audioArray sẽ chọn ra bit thứ 8 bằng cách & với 254 (để biến bit thứ 8 thành 0), khi đó
        # sẽ thực hiện toán tử ! với bit 0 đó bằng bit thông điệp, khi đó bit thứ 8 sẽ trở thành bit thông điệp
        for i, bit in enumerate(bits):
            audioArray[i] = (audioArray[i] & 254) | bit
        encodedAudio = bytes(audioArray)
        return self.saveToLocation(encodedAudio, audioLocation)
    def encodeImageAudio(self, audioLocationImage, imageToEncode) -> str:
        audioArray = self.convertToByteArray(audioLocationImage)
        image = Image.open(imageToEncode)
        new_image = image.resize((200, 200))
        new_image.save(imageToEncode)

        img = cv2.imread(imageToEncode, 2)
  
        ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
  
        bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        bits = list(map(int, ''.join([bin(j).lstrip('0b').rjust(13, '0') for i in bw_img for j in i])))
        for i, bit in enumerate(bits):
            audioArray[i] = (audioArray[i] & 254) | bit
        encodedAudio = bytes(audioArray)
        return self.saveToLocation2(encodedAudio, audioLocationImage)
    def decodeAudio(self, audioLocation) -> str:
        # Chuyển video đc mã hóa sang array
        audioArray = self.convertToByteArray(audioLocation)
        decodedArray = [audioArray[i] & 1 for i in range(len(audioArray))]
        # print(decodedArray)
        self.audio.close()
        decodeString = "".join(chr(int("".join(map(str, decodedArray[i:i + 13])), 2)) for i in range(0, len(decodedArray), 13)).split(
                "###")[0]
        return decodeString
    def decodeImageAudio(self, audioLocation) -> str:
        audioArray = self.convertToByteArray(audioLocation)
        decodedArray = [audioArray[i] & 1 for i in range(len(audioArray))]

        self.audio.close()
        decodeString = list((int("".join(map(str, decodedArray[i:i + 13])), 2)) for i in range(0, len(decodedArray), 13))
        
        arrSlice = []
        for i in range(len(decodeString)):
            if decodeString[i] != 255 and decodeString[i] != 0:
                arrSlice = decodeString[:i]
                break
        flatNumpyArray = np.array(arrSlice, dtype=np.uint8)
        arr2d = np.reshape(flatNumpyArray, (200,200))
        # data = Image.fromarray(arr2d)
        # data.save('output.png')
        cv2.imshow("Picture be hided", arr2d)

    def convertToByteArray(self, audioLocation):

        self.audio = wave.open(audioLocation, mode="rb")
        return bytearray(list(self.audio.readframes(self.audio.getnframes())))
