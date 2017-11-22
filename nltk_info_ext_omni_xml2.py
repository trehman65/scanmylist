##################################################################
# Project VisionX App
# Revision 3
# Reference doc: VisionX - OCR and NLP Module Diagram Rev 3.pdf
# Filename: nltk_info_ext_omni_xml.py 
# VERSION: 2.0
# (Introduced in Revision 3)
# Supervisor: Adnan-ul-Hassan adnan.ulhassan@visionx.io,
# Authors:    Sami-ur-Rehman sami@visionx.io,
#             Adil Usman adil.usman@visionx.io
##################################################################


import nltk
import sys
import re
import os
import csv
#import numpy
import string
import enchant
import enchant.checker
#import difflib
import json
from enchant.tokenize import get_tokenizer, EmailFilter, URLFilter, WikiWordFilter

from omnixmlconverter import OmniXmlToJsonConverter

import webcolors


def countVerbs(inputString):
    totalVerbs = 0
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString, tagset="universal")
    for token in taggedTokens:
        tag = token[1]
        #print token
        if tag.find("VERB") != -1:
            totalVerbs += 1
    return totalVerbs


def containsPOS(inputString, POS):
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString, tagset="universal")
    for token in taggedTokens:
        #print token
        tag = token[1]
        if tag.find(POS) != -1:
            return True
    return False

def containsPOS2(inputString, POS):
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString)
    for token in taggedTokens:
        #print token
        tag = token[1]
        if tag.find(POS) != -1:
            return True
    return False


def containsNoun(inputString):
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString, tagset="universal")
    for token in taggedTokens:
        tag = token[1]
        #print tag
        if tag.find("NOUN") != -1:
            return True
    return False


def containsVerb(inputString):
    tokenizedString = nltk.word_tokenize(inputString)
    taggedTokens = nltk.pos_tag(tokenizedString, tagset="universal")
    for token in taggedTokens:
        tag = token[1]
        if tag.find("VERB") != -1:
            #print token[1]
            return True
    return False


def evaluateString(inputString, dictSubjects):
    inputString = inputString.lower()
    # inputString=inputString.replace(' ','')

    if dictSubjects.__contains__(inputString):
        return "Subject"
    elif containsPOS2(inputString, "VBN") or containsPOS2(inputString, "VBD") or containsNoun(inputString) and not containsPOS(
            inputString, "VERB") and not (containsPOS(inputString, "ADP")
                                          or containsPOS(inputString, "DET")
                                          or containsPOS(inputString, "ADV")):
        #print inputString
        return "Item"
    elif containsPOS(inputString, "ADP") or containsPOS(
            inputString,
            "DET") or containsPOS(inputString, "PRT") or not containsPOS(
                inputString, "VERB") or not containsPOS(inputString, "NUM"):
        #print inputString
        return "Not a Product"
    # print inputString
    return "Not a Product"


def dict_check(inputString):
    #print inputString
    tknzr = get_tokenizer("en_US", [URLFilter, EmailFilter, WikiWordFilter])
    #d = enchant.DictWithPWL("en_US", "/opt/nltk_visionx/nltk/my_pwl.txt")
    d = enchant.DictWithPWL("en_US", "my_pwl.txt")
    exclude_list = [
        'Supplies', 'Supply', 'Materials', 'Material', 'Fee', 'Personal', 'Items', 'Mr.', 'Mr', 'Mrs', 'Algebra', 'Arts', 'History', 'Math', 'Maths',
        'Grade', 'Grades', 'Student', 'Students', 'Schools', 'School', 'com', 'www', 'Count', 'Counts'
        'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December', 'Elementary', 'Lists', 'List',
        'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth', 'Eleventh', 'Tweleveth',
		'1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th'
    ]
    for exclude in exclude_list:
        d.remove(exclude)
        d.remove(exclude.lower())
        d.remove(exclude.upper())
    #words = tknzr(inputString)
    words = nltk.word_tokenize(inputString)
    out = ''

    if len(words) > 0 and str.isdigit(str(words[0])):
        words.pop(0)
        #words = words[1:]
        if len(words) > 0 and str.isdigit(str(words[0])):
            words.pop(0)
            #words = words[1:]
            if len(words) > 0 and str.isdigit(str(words[0])):
                words.pop(0)
                #words = words[1:]

    if len(words) < 1:
        return ''

    sub_words = []
    for w in words:
        #print w
        sub_words_check = 1
        #print w

        if w == 'with' or w == 'for':
            break
        
        if len(w) > 2 and d.check(w):

            #print w
            sub_words = tknzr(w)
            for sub in sub_words:
                #print sub
                if not d.check(sub[0]) and not d.check(sub[0].lower()):
                    #print sub
                    sub_words_check = 0
            #print w
            if sub_words_check == 1:
                #print w
                out = out + w + ' '

    if len(out.strip()) > 2:
        return out.strip()
    else:
        return ''


def process(inputString):
    #print "BHAAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRRRRRRRRRRUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"

    wordlabel = []
    comment = ""

    line = inputString
    line = line.replace("\n", "")
    # strip spaces from stat and end of string
    line = line.strip()
    #orgline = line
    wordlabel.append(["Input", line])
    
    um=['rolls','sets','pkg','box','set','dozen','package','st','packs','pks','pkt','packet','pair','boxes','pkg.','packages','packages.','bx','ea','pk','gallon','canister','bottle','bottles','pack','pads','tray','ream','container','carton','tubes','bundle','pair','ct']

    mytags=[]
    regex = r"\d+\""
    match = re.findall(regex, line)
    
    if not len(match):
        regex = r"\d+\s+x+\s+\d"
        match = re.findall(regex, line)

    if not len(match):
        regex = r"\d+x+\d"
        match = re.findall(regex, line)
        
    if len(match): 
        mytags.append(match[0])
        wordlabel.append(["Dimensions", match[0]])

    for word in line.split():
        if word in webcolors.CSS3_NAMES_TO_HEX:
            mytags.append(word)
            wordlabel.append(["Color", word])
        if word.lower() in um:
            mytags.append(word)
            wordlabel.append(["UM", word])




    #print line
    line = line.replace('watercolor', 'water color')
    line = line.replace(' w/o ', 'without')
    line = line.replace(' w/', 'with ')
    line = line.replace(' Pkg ', ' Package ')
    line = line.replace(' pkg ', ' package ')
    line = line.replace(' Pk ', ' Pack ')
    line = line.replace(' pk ', ' pack ')
    line = line.replace(' pk', ' pack')
    line = line.replace(' packs ', ' pack ')
    line = line.replace(' Pkt ', ' Packet ')
    line = line.replace(' pkt ', ' packet ')
    line = line.replace(' Ea ', ' Each ')
    line = line.replace('Bx ', 'Box ')
    line = line.replace(' St ', ' Set ')
    line = line.replace(' sht ', ' sheet ')
    line = line.replace(' sht', ' sheet ')
    line = line.replace(' Pr ', ' Pair ')
    line = line.replace(' Dz', 'Dozen ')
    line = line.replace('Dz ', 'Dozen ')
    line = line.replace('dz ', 'dozen ')
    line = line.replace('oz.', 'ounce')
    line = line.replace(' x ', ' by ')
    line = line.replace('No. ', 'No-')



    line = re.sub(r'(?<![0-9])[/](?![0-9])', ' or ', line)
    line = re.sub(r'(?<![0-9])[0](?![0-9])', '', line)

    if line == '':
        return wordlabel

    # strip punctuation marks from start and end
    line = line.strip(string.punctuation)
    # strip spaces again from start and end
    line = line.strip()



    #input = line
    comment = line.split("(")[-1].split(")")[0]
    if comment != line:
        line = line.replace(comment, "")
        line = line.strip(string.punctuation)
        wordlabel.append(["Comment", comment])

    input = line



    if len(line) < 1:
        return wordlabel

    if (countVerbs(line) >= 2):
        #print wordlabel
        wordlabel.append(["Not a Product", line])
        return wordlabel
    else:
        input = re.sub(r'([^\s\w]|_)+', ' ', input)
        line = re.sub(r'([^\s\w]|_)+', ' ', line)

        if line.strip() == '' or input.strip() == '':
            return ''

        res_line = nltk.word_tokenize(input)
        tags = nltk.pos_tag(res_line)
        #print tags
        if (input.isdigit()):
            wordlabel.append(["Not a Product", line])
            #print wordlabel
            return wordlabel

        # first word is a number

        if tags[0][0].isdigit():

            if len(input.replace(tags[0][0], '', 1).strip()) < 1:
                input = dict_check(line)
                wordlabel.append(["Not a Product", line])
                #print wordlabel
                return wordlabel

            wordlabel.append(["Quantity", tags[0][0]])
            input = dict_check(input)
            #print input
            #wordlabel.append(["Item", input.replace(tags[0][0], '', 1).strip()])
            wordlabel.append(["Item", input.strip()])
            #print wordlabel
        # last word is quantity
        elif tags[len(tags) - 1][0].isdigit():
            wordlabel.append(["Quantity", tags[len(tags) - 1][0]])
            input = dict_check(input)
            #print input
            wordlabel.append(
                ["Item", input.strip(tags[len(tags) - 1][0]).strip()])
            #print wordlabel

        else:

            line = dict_check(line)
            #print line
            wordlabel.append(
                [evaluateString(line.strip(), dictSubjects), line])
        wordlabel.append(["tags",mytags])

    return wordlabel


abspath = os.getcwd()

dictSubjects = set()
#with open("/opt/nltk_visionx/nltk/dictSubjects.txt") as f:
with open("dictSubjects.txt") as f:
    content = f.readlines()
    for line in content:
        line = line.lower()
        if len(line) == 0:
            continue
        dictSubjects.add(line.replace("\n", ""))

requestID = sys.argv[1]

ocrlines_word_dict = {}
#with open('/opt/nltk_visionx/nltk/'+requestID + '_out_ocrlines_word_wbb.json') as data_file:
with open(requestID + '_out_ocrlines_word_wbb.json') as data_file:
    ocrlines_word_dict = json.load(data_file)

#print word_wbb_dict.keys()

out = 0
productList = []

line_counter = 0

for sentence in ocrlines_word_dict["result"]["sentences"]:
    #####################################
    word_wbb_dict = {}
    for word in sentence['words']:
        word_wbb_dict[word['word']] = word['boundingBox']
    # print word_wbb_dict

    ##########################################
    line = sentence["sentence"].strip()
    # line = unicode(line, "utf-8")

    line_counter += 1
    if len(line) > 3:
        if line.find("     "):
            parts = line.split("     ")
            for part in parts:

                if len(part) > 1:
                    out = process(part.strip())
        else:
            out = process(line)

    #################### REMOVING SPECIAL CHARACTERS FROM THE PRODUCT QUERY ###############
    # for ww in out:
    #     #print ww
    #     if ww[0] == 'Item':
    #         #print ww
    #         ww[1] = re.sub(r'[()0-9&#@!\/.,]+$', '', ww[1])
    #         #print ww
    #         #print

    thisitem = {}
    thisitem["Comment"] = ""
    thisitem["Label"] = "Not a Product"
    thisitem["Quantity"] = ""
    thisitem["Item"] = ""
    thisitem["Color"] = ""
    thisitem["UM"] = ""
    thisitem["Dimensions"] = ""
    thisitem["Tags"] = ""




    if type(out) is int:
        continue

    # print "New Sentence"
    for arr in out:
        
        if arr[0]=='tags':
            thisitem['Tags'] = arr[1];

        elif arr[0] != "Not a Product":
            thisitem[arr[0]] = arr[1].replace("\"", " ")

    quant_check = 0

    if (len(thisitem["Item"]) != 0):
        thisitem["Label"] = "Product"

    #process quantity
    if (len(thisitem["Quantity"]) == 0 and len(thisitem["Item"]) != 0):
        for t in nltk.pos_tag(
            [x.lower() for x in nltk.word_tokenize(thisitem["Item"])[:4]]):
            if t[1] == 'NNS':
                quant_check = 1

        if quant_check == 1:
            thisitem["Quantity"] = "Multiple"
        else:
            thisitem["Quantity"] = "1"


    pos_tags = nltk.pos_tag(
        [i.lower() for i in nltk.word_tokenize(thisitem["Item"])])
    if pos_tags:
        if pos_tags[-1][1] == 'IN' or pos_tags[-1][1] == 'CC':
            thisitem['Item'] = thisitem['Item'].rstrip(str(pos_tags[-1][0]))

    #################################################
    word_wbb_list = []
    x = ''

    thisitem['Item']=thisitem['Item'].replace(thisitem['UM'],'')
    thisitem['Item']=thisitem['Item'].replace(thisitem['Color'],'')


    for item in thisitem['Item'].split():
        word_wbb = {}
        word_wbb['word'] = item

        for k in word_wbb_dict.keys():
            if item in k:
                x = x + item + " "
                word_wbb['word_bounding_box'] = word_wbb_dict.get(k)
                break

        word_wbb_list.append(word_wbb)

    res_line = {}
    res_line['input'] = line

    if thisitem['Label'].strip() == "Product" and x != '':
        
        res_line['label'] = True
        #line = re.sub(r'^[0-9]$', '', res_line['product'])

        res_line['product'] = x.strip()  #thisitem['Item']
        res_line['quantity'] = thisitem['Quantity']
        res_line['words'] = word_wbb_list
        res_line['comment'] = thisitem['Comment']
        # res_line['color'] = thisitem['Color']
        # res_line['um'] = thisitem['UM']
        # res_line['dimensions'] = thisitem['Dimensions']
        res_line['tags'] = thisitem['Tags']

    else:
        res_line['label'] = False

        res_line['product'] = ''  #thisitem['Item']
        res_line['quantity'] = ''
        res_line['words'] = ''

    productList.append(res_line)
    #break

products = {}
products["lines"] = productList
nltkResult = {}
nltkResult["ie_result"] = products

# print productList
# json.dump(productList,outfile)
out_nltk_json = open(requestID + '_nltk.json', 'w')
json.dump(nltkResult, out_nltk_json)
