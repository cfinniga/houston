#houston_utils.py
# contains some extraneous things that we don't want cluttering up our main files

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup



class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

    
def val_match_dict_in_list(in_list, key, value):
    """ returns the index of a dict in a list of dicts where 
    the value of a particular entry matches"""
    for i, dic in enumerate(in_list):
            if dic[key] == value:
                break
    else: 
        i = -1
    return i 


