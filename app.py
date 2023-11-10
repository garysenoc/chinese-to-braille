  GNU nano 6.2                                                              flaskapp.py                                                                       




from flask import Flask, request, jsonify
import json
import numpy as np  
from pypinyin import pinyin, lazy_pinyin, Style
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def zhuyin_braille():
    zhuyinBraille = {}
    zhuyinCharacters = [' ','。','・','，','；','、','？','！','：','（','）','｛','｝','ㄅ','ㄆ','ㄇ',
        'ㄈ','ㄉ','ㄊ','ㄋ','ㄌ','ㄍ','ㄎ','ㄏ','ㄐ','ㄑ','ㄒ','ㄓ','ㄔ','ㄕ','ㄖ','ㄗ','ㄘ',
        'ㄙ','ㄧ','ㄨ','ㄩ','ㄚ','ㄛ','ㄜ','ㄝ','ㄞ','ㄟ','ㄠ','ㄡ','ㄢ','ㄣ','ㄤ','ㄥ','ㄦ',
        'ㄧㄚ','ㄧㄛ','ㄧㄝ','ㄧㄞ','ㄧㄠ','ㄧㄡ','ㄧㄢ','ㄧㄣ','ㄧㄤ','ㄧㄥ','ㄨㄚ','ㄨㄛ','ㄨㄞ',
        'ㄨㄟ','ㄨㄢ','ㄨㄣ','ㄨㄤ','ㄨㄥ','ㄩㄝ','ㄩㄢ','ㄩㄣ','ㄩㄥ','ˉ','ˊ','ˇ','ˋ','˙','、','‧','﹖','5',
        ' ','!','"','#','$','%','&','','(',')','*','+',',','-','.','/',
                '0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?','@',
                'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',
                'r','s','t','u','v','w','x','y','z','[','\\',']','^','_','’','\n',
                '{','⠼','}',"'"]
    
  zhuyinBrailleCharacters = ['⠀','⠤','⠤','⠆','⠰','⠠','⠕','⠇','⠒⠒','⠪','⠕','⠦','⠴','⠕','⠏','⠍',
        '⠟','⠙','⠋','⠝','⠉','⠅','⠇','⠗','⠅','⠚','⠑','⠁','⠃','⠊','⠛','⠓','⠚',
        '⠑','⠡','⠌','⠳','⠜','⠣','⠮','⠢','⠺','⠴','⠩','⠷','⠧','⠥','⠭','⠵','⠱',
        '⠾','⠴','⠬','⠢','⠪','⠎','⠞','⠹','⠨','⠽','⠔','⠒','⠶',
        '⠫','⠻','⠿','⠸','⠯','⠦','⠘','⠲','⠖','⠄','⠂','⠈','⠐','⠁','⠠','⠤','⠕',' ',
        '⠀','⠮','⠐','⠼','⠫','⠩','⠯','','⠷','⠾','⠡','⠬','⠠','⠤','⠨','⠌',
                '⠴','⠂','⠆','⠒','⠲','⠢','⠖','⠶','⠦','⠔','⠱','⠰','⠣','⠿','⠜','⠹','⠈',
                '⠁','⠃','⠉','⠙','⠑','⠋','⠛','⠓','⠊','⠚','⠅','⠇','⠍','⠝','⠕','⠏','⠟',
                '⠗','⠎','⠞','⠥','⠧','⠺','⠭','⠽','⠵','⠪','⠳','⠻','⠘','⠸','⠄','\n',
                '{','⠼','}',"⠄"]
    arrayLength = len(zhuyinCharacters)
    counter = 0 
    while counter < arrayLength:
        zhuyinBraille[zhuyinCharacters[counter]] = zhuyinBrailleCharacters[counter]
        counter = counter + 1

    return zhuyinBraille


@app.route("/", methods=["POST"])
def zhuyin_dotting_simple():
    text = request.form["text"]
    byte_string = text.encode('utf-8') 
    unicode_string = byte_string.decode('utf-8')  

    zhuyinBraille = zhuyin_braille()
    syllables = pinyin(unicode_string, style=Style.BOPOMOFO)
    flat_list = [item for sublist in syllables for item in sublist]
    zhuyinText = ''.join(flat_list)
    brailleString = ''

    i = 0
    while i < len(zhuyinText):
        char = zhuyinText[i].lower()

        # check if the current character is in zhuyinBraille
        if char in zhuyinBraille:
            brailleString = brailleString + zhuyinBraille[char]
        else:
            print(char, "does not exist in zhuyinBraille")

        # check if there is a pair of characters starting from the current character that exists in zhuyinBraille
        if i+1 < len(zhuyinText):
            substring = zhuyinText[i:i+2]
            if substring in zhuyinBraille:
                print(substring, "exists in zhuyinBraille")
                brailleString = brailleString + zhuyinBraille[substring]
                i += 1 # increment i by 1 to skip the second character in the substring

        i += 1

    return jsonify({"result":brailleString})

#def zhuyin_dotting_simple():
    #text = request.form["text"]
    #byte_string = text.encode('utf-8') 
    #unicode_string = byte_string.decode('utf-8')  
    
    #zhuyinBraille = zhuyin_braille()
    # print(zhuyinBraille)
    # zhuyinText = convert_huayu_zhuyin(unicode_string)
   # syllables = pinyin(unicode_string, style=Style.BOPOMOFO)
   # flat_list = [item for sublist in syllables for item in sublist]
   # zhuyinText = ''.join(flat_list)
   # brailleString = ''
   # for char in zhuyinText:
  #      char = char.lower()
 #       brailleString = brailleString + zhuyinBraille[char]
#    return jsonify({"result":brailleString})

if __name__== "__main__":
    app.run(host='0.0.0.0')

