from tkinter import *
from tkinter import filedialog
import tkinter
from tkinter.ttk import *
from LSBAudioStego import LSBAudioStego


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
        self.drawDecoding()
    def drawEncoding(self):
        # Label Mã Hóa
        self.encodeVar = StringVar()
        self.encodelabel = Label(root, textvariable=self.encodeVar)
        self.encodelabel.place(x=10, y=10)
        self.encodeVar.set("Mã hóa ")
        # Nút chọn File âm thanh
        self.selectFileButton = Button(self, text="Chọn file âm thanh để mã hóa văn bản", command=self.selectFile)
        self.selectFileButton.place(x=10, y=50)
        # nút chọn file hình ảnh
        self.selectFileButton = Button(self, text="Chọn file âm thanh để mã hóa hình ảnh", command=self.selectFileAudioImage)
        self.selectFileButton.place(x=10, y=120)
        # Label lưu đường dẫn file
        self.var = StringVar()
        self.label = Label(root, textvariable=self.var, relief=RAISED)
        self.label.place(x=10, y=80)

        self.var1 = StringVar()
        self.label = Label(root, textvariable=self.var1, relief=RAISED)
        self.label.place(x=10, y=160)

        self.var2 = StringVar()
        self.label = Label(root, textvariable=self.var2, relief=RAISED)
        self.label.place(x=10, y=280)
        
        # Label nhập văn bản cần giấu
        self.boxVar = StringVar()
        self.boxlabel = Label(root, textvariable=self.boxVar)
        self.boxlabel.place(x=10, y=180)
        self.boxVar.set("Nhập văn bản cần giấu")
        # Text ghi văn bản cần giấu
        self.entryText = Entry(root)
        self.entryText.place(x=10, y=200)
        self.entryText.insert(0, "")
        
        # Nút mã hóa
        self.encodeButton = Button(self, text="Mã hóa", command=self.encode)
        self.encodeButton.place(x=10, y=320)

        # encoded  location label
        self.enocdedLocation = StringVar()
        self.locationOfEncodeFile = Label(root, textvariable=self.enocdedLocation)
        self.locationOfEncodeFile.place(x=10, y=280)


    def drawDecoding(self):
        # decode Label
        self.decodeVar = StringVar()
        self.decodelabel = Label(root, textvariable=self.decodeVar)
        self.decodelabel.place(x=650, y=10)
        self.decodeVar.set("Giải mã ")

        # creating a button instance
        self.selectFileDecodeButton = Button(self, text="Chọn file để giải mã văn bản", command=self.selectFileDecode)
        self.selectFileDecodeButton.place(x=650, y=100)
        # creating a button instance
        self.selectFileDecodeButton = Button(self, text="Chọn file để giải mã hình ảnh", command=self.selectFileDecodeAudioImage)
        self.selectFileDecodeButton.place(x=650, y=160)
        # file location label
        self.decodeFileVar = StringVar()
        self.decodeFileLabel = Label(root, textvariable=self.decodeFileVar, relief=RAISED)
        self.decodeFileLabel.place(x=650, y=140)

        # file location label
        self.decodeFileVar2 = StringVar()
        self.decodeFileLabel = Label(root, textvariable=self.decodeFileVar2, relief=RAISED)
        self.decodeFileLabel.place(x=650, y=190)

        self.decodeButton = Button(self, text="Giải mã", command=self.decode)
        self.decodeButton.place(x=650, y=320)
        #
        # decoded text label
        self.decodedString = StringVar()
        self.decodedStringlabel = Label(root, textvariable=self.decodedString, font=(None, 40))
        self.decodedStringlabel.place(x=650, y=350)
        # chon hinh anh
        self.selectFileButton = Button(self, text="Chọn file hình ảnh cần mã hóa", command=self.selectImageEncode)
        self.selectFileButton.place(x=10, y=250)

        self.lengthText2 = StringVar()
        self.lengthlabel2 = Label(root, textvariable=self.lengthText2)
        self.lengthlabel2.place(x=10, y=220)
        #
    # Hàm thoát
    def client_exit(self):
        exit()
    # Hàm chọn file
    def selectFile(self):
        # file selection
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.wav"), ("all files", "*.*")))
        self.fileSelected = root.filename
        self.var.set(root.filename)
    def selectFileAudioImage(self):
        # file selection
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.wav"), ("all files", "*.*")))
        self.fileAudioImageSelected = root.filename
        self.var1.set(root.filename)
    # Ham chon anh de ma hoa
    def selectImageEncode(self):
        # file selection
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.fileImageEncode = root.filename
        self.var2.set(root.filename)
    # Hàm chọn file để giải mã
    def selectFileDecode(self):
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.wav"), ("all files", "*.*")))
        self.fileSelcetedForDecode = root.filename
        self.decodeFileVar.set(root.filename)
    #Hàm chọn file giải mã hình ảnh
    def selectFileDecodeAudioImage(self):
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.wav"), ("all files", "*.*")))
        self.fileSelcetedForDecodeAudioImage = root.filename
        self.decodeFileVar2.set(root.filename)
    
    # Hàm mã hóa
    def encode(self):
        # select algo to encode
        # algo = PhaseEncodingAudioStego()
        # result = algo.encodeAudio(self.fileSelected, self.entryText.get())
        # Textself.enocdedLocation.set(result)
        # Chọn phương pháp mã hóa LSB
        algo = LSBAudioStego()
        result = algo.encodeAudio(self.fileSelected, self.entryText.get())
        result2 = algo.encodeImageAudio(self.fileAudioImageSelected, self.fileImageEncode)
        self.enocdedLocation.set(result)
        self.enocdedLocation.set(result2)
    # Hàm giải mã
    def decode(self):
        # select algo to decode
        # algo = PhaseEncodingAudioStego()
        # result = algo.decodeAudio(self.fileSelcetedForDecode)
        # self.decodedString.set(result)
        # Chọn phương pháp giải mã từ LSB
        algo = LSBAudioStego()
        result = algo.decodeAudio(self.fileSelcetedForDecode);
        result2 = algo.decodeImageAudio(self.fileSelcetedForDecodeAudioImage);
        self.decodedString.set(result)

root.geometry("1100x500")
app = Window(root)
root.mainloop()
