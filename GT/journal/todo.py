from __future__ import with_statement
import re, json, datetime, os, shutil
from collections import defaultdict
import logging
import poodledo
from poodledo.apiclient import ApiClient, PoodledoError
from poodledo.cli import do_login

class Action(object):
    pass

class Todo(Action):
    def __init__(self, debug=False):
        try:
            self.client = do_login()
        except PoodledoError as e:
            print e
            exit(1)

class Shopping(Action):
    def __init__(self, debug=False):
        try:
            self.client = do_login()
        except PoodledoError as e:
            print e
            exit(1)

        if debug:
            self.folder_name = "test-Shopping"
        else:
            self.folder_name = "Shopping"

        try:
            self.folder_id = self.client.getFolder(self.folder_name)['id']
        except PoodledoError:
            self.client.addFolder(self.folder_name)
            self.folder_id = self.client.getFolder(self.folder_name)['id']

    def disp(self):
        for t in self.client.getTasks(cache=True):
            if 'folder' in t and t['folder'] == self.folder_id:
                print t

    def addItem(self, title):
        self.client.addTask(title=title, folder = self.folder_name)
