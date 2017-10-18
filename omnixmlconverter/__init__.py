import io
import os
import sys
import json
from collections import OrderedDict

try:
    from lxml.etree import tostring as tostring, fromstring
    from lxml.doctestcompare import LXMLOutputChecker
    import lxml.html
    import lxml.etree
    import xml.etree.ElementTree as ET
    import xmljson
    from dictrefractor import DictRefractor
except ImportError as ex:
    print 'OmniConverter ImportError: ', format(ex)


class OmniXmlToJsonConverter():
    '''Usage for the OmniXmlToJsonConverter class \n
    Step 0-A: Provide the name of the Xml file with OCR result from the Omni OCR Engine \n
    \t\t            Example: omni_result_xml_file = "./omni_xml_file.xml" \n
    Step 0-B: Provide the name of the Output Json file for the converter \n
    \t\t            Example: omni_result_json_file = "omni_json" \n
    Step 1: Steps initialize OmniXmlToJsonConverter with the required XML convention \n
    \t\t            Default: XML_Convention = xmljson.Yahoo(dict_type=OrderedDict) \n
    \t\t            Example: omniXml2Json = OmniXmlToJsonConverter() \n
    Step 2: Open the Xml file with OCR result from the Omni OCR Engine \n 
    \t\t            Example: omniXml2Json.readOmniXmlFile(omni_result_xml_file) \n
    Step 3: Call the converter to convert xml file to json format \n
    \t\t            Example: omniXml2Json.convertToJson() \n
    Step 4: Get the converted omni_json \n
    \t\t            Example: omnni_json = omniXml2Json.getJson() \n
    Step 4: (Optional) save the omni_json.json to a File \n
    \t\t            Example: omniXml2Json.saveOmniJson(omni_result_json_file) \n
    '''

    def __init__(self, xml_convention=None):
        if xml_convention is None:
            self.xml_convention = xmljson.Yahoo(dict_type=OrderedDict)
        elif isinstance(xml_convention, xmljson.Parker):
            print 'OmniXmlToJson: XML Parker convention not supported'
            exit()
            return

        self.__omni_xml_file = ''
        self.__omni_json_file = ''
        self.__omni_tree = None
        self.__omni_json_dict = {}
        self.__root_key = 'document'
        self.__refractor_string = ''
        return

    def getJson(self):
        return self.__omni_json_dict

    def readOmniXmlFile(self, filename):
        if filename.find('.xml') == -1:
            filename = filename + '.xml'
        self.__omni_xml_file = filename
        with open(self.__omni_xml_file) as omni_xml_file:
            self.__omni_tree = ET.parse(omni_xml_file)
        return

    def convertToJson(self, xml_file=None, reformat_omni=True):
        if xml_file is not None:
            self.readOmniXmlFile(xml_file)
        if self.__omni_tree is None:
            print 'OmniError: XML file ReadError, Specify XML file before conversion'
            exit()
        root = self.__omni_tree.getroot()
        self.__omni_json_dict = self.xml_convention.data(root)

        if reformat_omni:
            self.__reformatOmniJson()
        return

    def saveOmniJson(self, filename='omni_json'):
        if filename.find('.json') == -1:
            filename = filename + '.json'
        self.__omni_json_file = filename
        with open(self.__omni_json_file, 'w') as omni_to_json_file:
            json.dump(self.__omni_json_dict, omni_to_json_file)
        return

    def __getReformatString(self):
        for key, value in self.__omni_json_dict.iteritems():
            if key.find(self.__root_key) != -1:
                # reformat_string = key.split('document')[0]
                truncate_length = len(self.__root_key)
                self.__refractor_string = key[:-truncate_length]
                break
        return

    def __reformatOmniJson(self):
        self.__getReformatString()
        refractorJson = DictRefractor()
        refractorJson.removeStringFromKeys(
            data=self.__omni_json_dict, remove_string=self.__refractor_string)
        refractorJson.changeValueTypeForKeys(data=self.__omni_json_dict, keys_list=['ln', 'wd', 'textZone'])
        return

