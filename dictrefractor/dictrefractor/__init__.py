import io
import os
import sys
import json

class DictRefractor():
    def __init__(self):
        self.__remove_string = ''
        self.__operator = ''
        self.__list_of_keys = []
        return

    def __renameDictKey(self, dictionary, old_key, new_key):
        try:
            dictionary[new_key] = dictionary.pop(old_key)
            return True
        except Exception as ex:
            print 'Error: ', format(ex)
            return False

    def __removeStringFromKey(self, dictionary, old_key):
        # print key, '***'
        Remove_String = self.__remove_string
        if old_key.find(Remove_String) != -1:
            try:
                new_key = old_key.split(Remove_String)[1]
                # old_key = key
                self.__renameDictKey(dictionary, old_key, new_key)
            except ValueError as ex:
                print 'ValueError: ', ex
        else:
            pass
        return

    def __changeValueTypeToList (self, dictionary, key):
        if key in self.__list_of_keys:
            # print "key match: ", key
            if isinstance(dictionary[key], (str, int)):
                return
            if isinstance(dictionary[key], list):
                return
            if isinstance(dictionary[key], dict):
                value = dictionary[key]
                dictionary[key] = [ value ]
                return
        return

    def __applyOperator(self, dictionary, key):
        if self.__operator == 'remove_string':
            self.__removeStringFromKey(dictionary, key)
        elif self.__operator == 'change_value_type_list':
            self.__changeValueTypeToList(dictionary, key)
        return

    def __reformatKeysInDict(self, dictionary):
        # new_keys = []
        # Remove_String = self.__remove_string
        new_key = ''
        if isinstance(dictionary, (str, int)):
            return
        try:
            for key, value in dictionary.iteritems():
                self.__applyOperator(dictionary, key)
                continue
        except Exception as ex:
            print 'Error: ', format(ex)
        return new_key

    def __reformatKeysInListOfDict(self, dictList):
        # new_keys = []
        Remove_String = self.__remove_string
        new_key = ''
        if isinstance(dictList, (str, int)):
            return
        try:
            for key, value in dictList.iteritems():
                self.__applyOperator(dictList, key)
                continue
        except Exception as ex:
            print 'Error:', format(ex)
        return new_key

    def __reformatKeysInList(self, dictList=[]):
        try:
            for dictionary in dictList:
                self.__reformatKeysInListOfDict(dictionary)
        except Exception as ex:
            print 'Error:', format(ex)
        return

    def __reformatKeys(self, data):
        if data == False or data == None:
            return

        if isinstance(data, str):
            return

        if isinstance(data, int):
            return

        if isinstance(data, list):
            for item in data:
                self.__reformatKeys(item)
            self.__reformatKeysInList(data)
            return

        if isinstance(data, dict):
            for key, value in data.iteritems():
                self.__reformatKeys(data[key])
            self.__reformatKeysInDict(data)
            return
        return

    def removeStringFromKeys(self, data, remove_string):
        self.__remove_string = remove_string
        self.__operator = 'remove_string'
        self.__reformatKeys(data)

    def changeValueTypeForKeys(self, data, keys_list = ['']):
        self.__list_of_keys = keys_list
        self.__operator = 'change_value_type_list'
        self.__reformatKeys(data)

################################################################
