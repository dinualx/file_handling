import os
import pdfplumber
import docx
from pathlib import PureWindowsPath
import platform


class FILE:

    def __init__(self):
        self.basename = None
        self.fileextension = None
        self.extensions = ["csv", "txt", "pdf", "docx"]
        self.allwords = []
        self.longestword = []
        self.longesttransposed = []
        self.longestlength = ""
        self.mykey = 3


    def reinit(self):
        self.__init__()

    def extractbasename(self, path):
        if platform.system() =='Windows':
            tail = PureWindowsPath(path).name
        else:
            tail = os.path.basename(path)
            self.basename = tail
        return tail

    def getfileextension(self, path):
        filename = self.extractbasename(path)
        splitted = filename.split('.')
        self.fileextension = splitted[1]
        return self.fileextension



    def validatefiletype(self, path):
        extension = self.getfileextension(path)
        if extension not in self.extensions:
            raise ValueError("Invalid file type, extension must be .csv, .txt, .pdf or .docx")
        return True

    def getallwords(self, path):
        if self.validatefiletype(path):
            pass
            # print('The ' + self.extractbasename(path) + ' file is supported, it is a .' + self.getfileextension(path) + ' type file, following to read all words from it')
            if self.getfileextension(path) == 'txt':
                # print('This is a .txt file')
                try:
                    with open(path, 'r', encoding='utf8') as file:
                        data = file.read()
                        self.allwords = data.split()
                except FileNotFoundError:
                    raise FileNotFoundError("Sorry, the provided file does not exist, check file path or that the file exists!")
                except Exception as e:
                    raise Exception("Sorry, the file is password protected or corrupted or for any other reason it cannot be opened!")
            elif self.getfileextension(path) == 'csv':
                # print('This is a .csv file')

                try:
                    f = open(path, 'r')
                    data = f.read()
                    new_data = data.replace('"', '')
                    new_data2 = new_data.replace(',', ' ')
                    new_data3 = new_data2.replace('.', ' ')
                    self.allwords = new_data3.split()
                except FileNotFoundError:
                    raise FileNotFoundError("Sorry, the provided file does not exist, check file path or that the file exists!")
                except Exception as e:
                    raise Exception("Sorry, the file is password protected or corrupted or for any other reason it cannot be opened!")
            elif self.getfileextension(path) == 'docx':
                # print('This is a .docx file')
                try:
                    doc = docx.Document(path)
                    fullText = []
                    for para in doc.paragraphs:
                        fullText.append(para.text)
                    data = ''.join(fullText)
                    punc = ''',!()-[]{};:'"\<>./?@#$%^&*_~'''
                    for ele in data:
                        if ele in punc:
                            test_str = data.replace(ele, " ")
                    new_data2 = test_str.replace(',', ' ')
                    word_list = new_data2.split()
                    self.allwords = word_list
                except docx.opc.exceptions.PackageNotFoundError:
                    raise FileNotFoundError("Sorry, the provided file does not exist, check file path or that the file exists!")
                except Exception as e:
                    raise Exception("Sorry, the file is password protected or corrupted or for any other reason it cannot be opened!")
            elif self.getfileextension(path) == 'pdf':
                # print('This is a .pdf file')
                try:
                    with pdfplumber.open(path) as pdf:
                        fullText = []
                        for page in pdf.pages:
                            Text = page.extract_text()
                            words = Text.split()
                            fullText.extend(words)
                        self.allwords = fullText
                except FileNotFoundError:
                    raise FileNotFoundError("Sorry, the provided file does not exist, check file path or that the file exists!")
                except Exception as e:
                    raise Exception("Sorry, the file is password protected or corrupted or for any other reason it cannot be opened!")

        if len(self.allwords) > 0:
            pass
            # print('this is the list with all the words: {}'.format(self.allwords))
            # print('this is the number of all the words from the file: {}'.format(len(self.allwords)))
        else:
            raise Exception("ERROR: The provided file does not contain any text!")
        return self.allwords


    def findlongestwords(self, path):
        sorted_list = sorted(self.getallwords(path), key=len, reverse=True)
        max_length = len(sorted_list[0])
        longest = []
        longestlength = ""
        my_dict = {}
        for word in sorted_list:
            if len(word) == max_length:
                longest.append(word)
                longestlength = len(word)
        for word in longest:
            cnt = longest.count(word)
            if cnt > 1 and word not in my_dict:
                my_dict[word] = cnt
        list = []
        for key in my_dict.keys():
            list.append(key)
        if len(list)>0:
            self.longestword = list
            # print('this is the list with the longest words: {}'.format(list) + ', and this is the longest length: {}'.format(longestlength))
        else:
            self.longestword = longest
            # print('this is the list with the longest words: {}'.format(longest) + ', and this is the longest length: {}'.format(longestlength))
        return self.longestword

    def getlongestlength(self, path):
        list = self.findlongestwords(path)
        self.longestlength = len(list[0])
        return self.longestlength


    def transposeword(self, word):
        key = self.mykey
        ciphertext = [''] * key
        for col in range(key):
            pointer = col
            while pointer < len(word):
                ciphertext[col] += word[pointer]
                pointer += key
            transposed = ''.join(ciphertext)
        return transposed


    def transposelongest(self, path):
        if self.getlongestlength(path) >= 2:
            pass
        else:
            raise Exception("The largest word does not have at least 2 letters for it to be transposed")
        transposed_list = []
        list = self.findlongestwords(path)
        for word in list:
            transposed_word = self.transposeword(word)
            transposed_list.append(transposed_word)
        print('this is the list with the longest words transposed: {}'.format(transposed_list))
        return transposed_list

    def showlongestandtransposed(self, path):
        longest = self.findlongestwords(path)
        longest_transposed = self.transposelongest(path)
        print('longest words:{}'.format(longest) + ' longest transposed words:{}'.format(longest_transposed))
        return(longest,longest_transposed)





v = FILE()
g = FILE()
h = FILE()
k = FILE()
# v.extractbasename("/home/alex/alex/practice/SampleTextFile.txt")
# v.validatefiletype("/home/alex/alex/practice/SampleTextFile.txt")
# v.getfileextension("/home/alex/alex/practice/SampleTextFile.txt")
# v.getallwords("/home/alex/alex/practice/SampleTextFile.txt")
# g.getallwords("/home/alex/alex/practice/addresses.csv")
# h.getallwords("/home/alex/alex/practice/samplefile.docx")
# k.getallwords("/home/alex/alex/practice/sample2.pdf")
# k.findlongestword("/home/alex/alex/practice/sample2.pdf")
# v.findlongestwords("/home/alex/alex/practice/SampleTextFile.txt")
# g.findlongestwords("/home/alex/alex/practice/industry.csv")
# v.transposelongest("/home/alex/alex/practice/SampleTextFile.txt")
# k.transposelongest("/home/alex/alex/practice/sample2.pdf")
# k.findlongestwords("/home/alex/alex/practice/sample2.pdf")
# k.showlongestandtransposed("/home/alex/alex/practice/sample2.pdf")
# v.showlongestandtransposed("/home/alex/alex/practice/SampleTextFile.txt")
# h.showlongestandtransposed("/home/alex/alex/practice/samplefile.docx")
# g.showlongestandtransposed("/home/alex/alex/practice/addresses.csv")
# v.transposeword('transposition')
# k.showlongestandtransposed("D:\\files\\addresses.csv")
# k.showlongestandtransposed("D:\\files\\textsamplefile.txt")
# k.showlongestandtransposed("D:\\files\\samplefile.docx")
