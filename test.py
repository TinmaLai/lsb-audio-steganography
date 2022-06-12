from quopri import decodestring
from tkinter import *
from tkinter import filedialog
import tkinter
from tkinter.ttk import *
import numpy as np
import cv2
from PIL import Image

root = Tk()
class Window(tkinter.Frame):
    def __init__(self, master = None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()
    def init_window(self):
        self.master.title("Demo giấu tin âm thanh bằng mã hóa pha")
        self.pack(fill=BOTH, expand=1)
        self.drawEncoding()
    def drawEncoding(self):
        # Label Mã Hóa
        self.encodeVar = StringVar()
        self.encodelabel = Label(root, textvariable=self.encodeVar)
        self.encodelabel.place(x=10, y=10)
        self.encodeVar.set("Mã hóa ")
        # Nút chọn File
        self.selectFileButton = Button(self, text="Chọn file hình ảnh cần mã hóa", command=self.selectImageEncode)
        self.selectFileButton.place(x=10, y=50)

        # Label lưu đường dẫn file
        self.var = StringVar()
        self.label = Label(root, textvariable=self.var, relief=RAISED)
        self.label.place(x=10, y=80)

        self.encodeButton = Button(self, text="Mã hóa", command=self.imageToBinary)
        self.encodeButton.place(x=10, y=300)

        self.enocdedLocation = StringVar()
        self.locationOfEncodeFile = Label(root, textvariable=self.enocdedLocation)
        self.locationOfEncodeFile.place(x=10, y=280)
    # Hàm thoát
    def client_exit(self):
        exit()
    # Hàm chọn file
    def selectImageEncode(self):
        # file selection
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.fileImageEncode = root.filename
        self.var.set(root.filename)
    def imageToBinary(self):
        imgSelect = self.fileImageEncode

        image = Image.open(imgSelect)
        new_image = image.resize((100, 100))
        new_image.save(imgSelect)

        img = cv2.imread(imgSelect, 2)
  
        ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
  
# converting to its binary form
        bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
  
        # cv2.imshow("Binary", bw_img)
        # np_img = ~np_img  # invert B&W
        # np_img[np_img > 0] = 1

        # array = [[1,2,3],[4,5,6],[300]]
        # bw_img[len(bw_img)-1].append([300])
        # markArray = np.full((1,100),300)
        # np.append(bw_img,np.array(markArray), axis=0)
        audioArray = []
        for i in range(10000000):
            audioArray.append(1)
        
        bits = list(map(int, ''.join([bin(j).lstrip('0b').rjust(13, '0') for i in bw_img for j in i])))
        for i, bit in enumerate(bits):
            audioArray[i] = (audioArray[i] & 254) | bit


        decodedArray = [audioArray[i] & 1 for i in range(len(audioArray))]
        decodeString = list((int("".join(map(str, decodedArray[i:i + 13])), 2)) for i in range(0, len(decodedArray), 13))
        
        arrSlice = []
        for i in range(len(decodeString)):
            if decodeString[i] != 255 and decodeString[i] != 0:
                arrSlice = decodeString[:i]
                break
        flatNumpyArray = np.array(arrSlice, dtype=np.uint8)
        arr2d = np.reshape(flatNumpyArray, (100,100))
        # data = Image.fromarray(arr2d)
        # data.save('output.png')
        print(arr2d)
        print(bw_img)
        cv2.imshow("gfsgfdg", arr2d)
root.geometry("700x500")
app = Window(root)
root.mainloop()
