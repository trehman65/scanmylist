##################################################################
# Project VisionX App
# Revision 3
# Reference doc: VisionX - OCR and NLP Module Diagram Rev 3.pdf
# Filename: omni-xml-to-json.py 
# VERSION: 2.0
# (Introduced in Revision 3)
# Supervisor: Adnan-ul-Hassan adnan.ulhassan@visionx.io,
# Authors:    Sami-ur-Rehman sami@visionx.io,
#             Adil Usman adil.usman@visionx.io
##################################################################

import sys
import os
import json

from omnixmlconverter import OmniXmlToJsonConverter



requestID = sys.argv[1]

omni_xml_converter = OmniXmlToJsonConverter()
# $1_out_omni.xml
omni_xml_converter.convertToJson(requestID + '_out_omni.xml')

omni_xml_converter.saveOmniJson(requestID + '_out_omni.json')

ocrlines_word_dict = {}

omni_json = omni_xml_converter.getJson()

text_zones = omni_json['document']['page']['zones']['textZone']

ocrlines_word_dict = {}
ocrlines_word_dict['sentences'] = []
sentence_count = -1
sentences_list = []
for textZone in text_zones:

    # mistake
    lines = textZone['ln']
    if isinstance(lines, list):
        for line in lines:
            sentence = ''
            wordsList = []
            sentence_bounding_box = {}
            sentence_dict = {}
            words = line['wd']

            for word in words:
                word_dict = {}
                word_bounding_box = {}
                word_content = ''
                try:
                    word_content = word['content']
                except Exception as ex:
                    # print 'Error: ', format(ex)
                    try:
                        wdd = word['run']
                        if isinstance(wdd, dict):
                            try:
                                word_content = wdd['content']
                            except Exception as exc:
                                # print 'Error: ', format(exc)
                                pass

                        elif isinstance(wdd, list):
                            try:
                                for w in wdd:
                                    word_content = word_content + w['content']
                            except Exception as exc:
                                # print 'Error: ', format(exc)
                                pass
                        else:
                            try:
                                word_content = wdd
                            except Exception as exc:
                                # print 'Error: ', format(exc)
                                pass
                    except Exception as excep:
                            # print 'Error: ', format(excep)
                            pass

                sentence = sentence + word_content + ' '
                word_bounding_box['top'] = word['t']
                word_bounding_box['left'] = word['l']
                word_bounding_box['bottom'] = word['b']
                word_bounding_box['right'] = word['r']
                # word_dict = {}
                word_dict['word'] = word_content
                word_dict['boundingBox'] = word_bounding_box
                wordsList.append(word_dict)

            sentence_bounding_box['top'] = line['t']
            sentence_bounding_box['left'] = line['l']
            sentence_bounding_box['bottom'] = line['b']
            sentence_bounding_box['right'] = line['r']

            sentence_count = sentence_count + 1
            sentence_dict['sentenceID'] = sentence_count
            sentence_dict['sentence'] = sentence
            sentence_dict['sentenceBoundingBox'] = sentence_bounding_box
            sentence_dict['words'] = wordsList
            sentences_list.append(sentence_dict)

ocrlines_word_dict['sentences'] = sentences_list

with open(requestID + '_out_ocrlines_word_wbb.json', 'w') as out_ocrlines_json:
    json.dump(ocrlines_word_dict, out_ocrlines_json)
