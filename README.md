Testing the following functionalities for file handling:
Read input from a file of words
Find the longest word in the file
Transpose the letters in the longest word
Show the longest word and the longest word transposed 

Below there are my assumptions:
I considered these files could be passed in by the user for processing:
- .txt, .csv, .pdf, .docx
- if a different type of file is passed in, an error will be raised
- if the file path is wrong and the file cannot be found, I handled this case to raise an error with the specific message
- if the file cannot be opened for various reasons like password protected or corrupted or any other reason, for this case it will be an error message raised with a specific message
- if no text is found in the file, an error will be raised with a specific message


import os
import pdfplumber
import docx
from pathlib import PureWindowsPath
import platform


the above modules and libraries needed for building the code
I have created a class for all the methods to be part of this FILE class
class FILE:

below there are the class variables that I considered I need, initialized within the constructor init method

    def __init__(self):
        self.basename = None
        self.fileextension = None
        self.extensions = ["csv", "txt", "pdf", "docx"]
        self.allwords = []
        self.longestword = []
        self.longesttransposed = []
        self.longestlength = ""
        self.mykey = 3

I created a reinit method which does the same thing as the init constructor, for using it in the class methods if needed. Of course, this reinit method will reset to default the class variables for a specific instance

    def reinit(self):
        self.__init__()
        
This method below it is used to extract only the file name along with its extension, from the provided path depending on operating system, MACOS, Linux or Windows, I called built-in methods for windows I called a method using PureWindowsPath and platform libraries for MACOS and Linux I called a method using os library        

    def extractbasename(self, path):
        if platform.system() =='Windows':
            tail = PureWindowsPath(path).name
        else:
            tail = os.path.basename(path)
            self.basename = tail
        return tail

The method below it is used to extract only the extension from the file provided file path. without the dot character
First, the whole filename is extracted with its extension, splitted the filename in two, the actual filename and its extension, needing only its extension, that means it is the second item from splitted list, list start from index 0, so list[1], also this function will return the extension


    def getfileextension(self, path):
        filename = self.extractbasename(path)
        splitted = filename.split('.')
        self.fileextension = splitted[1]
        return self.fileextension


The method below it is used to validate file type based onits extension. I used a variable to store the instance self.fileextension variable by calling getfileextension(path), if the extension is not in the expected values, an error is raised, if the method runs successfully, it will return True value


    def validatefiletype(self, path):
        extension = self.getfileextension(path)
        if extension not in self.extensions:
            raise ValueError("Invalid file type, extension must be .csv, .txt, .pdf or .docx")
        return True


The below methos will retrieve all words from the provided file. First, we validate the file type using the validatefiletype method; if the validatefiletype method fails, getallwords will practically fail at this step; I treated each type of file in particular. I placed the code in a try except block to handle 2 error situation, the first when file is not found; file could not be found due to wrong path or wrong filename in the path or anything wrong with the path; the second handled situation practically when the qfile cannot be opened for any other reasons, like password protected, corrupted or anything else that prevents the file to be opened; the words are placed in a list; I populated self.allwords instance variable with the list. After file type is opened and we retrieve all words in a list I have made a check step for this, to see if the words list is empty or not. If empty, an error will be raised that the provided file does not contain text. I raised an error here because there is no point in going further with anything that involves text processing if there is no text.



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


For finding the longest words, because can be multiple words which have the same lenght, the below method. I used what self.getallwords returns - meaning the list with all words having this list, I sorted it to start with the longest word first, that is why reverse is True here, having the first word as the longest, after it could be multiple words having the same maximum length so the max length is the length of the first word from the sorted list every word that has this length will be placed in the list with longest words, if the word has the maxim length so now we have a list with the longest words, longest[]
it is possible to have duplicates in it, if not we will populate self.longestword with longest if we have duplicates in this list, I created a dictionary having as keys the words that are duplciated, and having as values the count for each word. So having these organized in this manner, I retrieve from this dictionary only the keys, these keys being the words without duplication. And I populate self.longestword with keys from this dictionary 



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


The method below is to find out what is the length of the logest word. I have used what self.findlongestwords return to get the length of the first word from the list, which is the longest.


    def getlongestlength(self, path):
        list = self.findlongestwords(path)
        self.longestlength = len(list[0])
        return self.longestlength


For transposing the words I have created a transposition cypher, it takes as argument the word that you want to transposed.
I have defined a key, took it from the self.mykey instance variable, which is the same for all instances; what this function does, it arranges the letters from the word one by one into a matrix which has 3 columns; I have 3 columns because the column number is equal with the key, so let's take an example, if we have the word demonstration, it will be arranged in this manner:it will be a first line created from d-e-m, because we reached the key length value, 
#which is 3, another line is started under the first line, o-n-s, then anther one, under it t-r-a, the another one t-i-o, and eventually the last line which has only one letter and 2 blanks, n.
d-e-m
o-n-s
t-r-a
t-i-o
n
after having this arrangement, the word is remade by joining each column, so we will have d-o-t-t-n-e-n-r-i-m-s-a-o so, instead of demonstration we will have dottnenrimsao.

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


This method is to transpose the longest word, it uses the transposeword method from above, we need at least 2 letters in the word for it to be transpossed, or else an error is raised.



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


This method prints and returns the longest word and the longest word transposed.


    def showlongestandtransposed(self, path):
        longest = self.findlongestwords(path)
        longest_transposed = self.transposelongest(path)
        print('longest words:{}'.format(longest) + ' longest transposed words:{}'.format(longest_transposed))
        return(longest,longest_transposed)


I ran my project in a Windows environment. As a CI tool I used Jenkins. As framework I used robot.
The project contains the following:
The FILE python file, which contains all the methods written in python
The file_handling robot file, which contains all the tests written in robot
The run bat file, which contains the windows batch commands to run the project
A folder with the files under test that I used in my test cases, there are a .txt, a .pdf, a .csv and a .docx file


For python you need to install the python modules that I have used, with pip install and the module name.
In my robot test cases I have used local paths for the files, you will have to change them accordingly to where you will
put the files locally on ypur machine.
In my run.bat file I have used commands to go to the project location, you will have to do the same thing for this, 
to modify the path from the command accordingly.









