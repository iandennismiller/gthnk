# (c) 2013 Ian Dennis Miller
# -*- coding: utf-8 -*-

from __future__ import with_statement
import re, json, datetime, os, shutil, urllib2, logging
from collections import defaultdict
import poodledo
from poodledo.apiclient import ApiClient, PoodledoError
from poodledo.cli import do_login
from poodledo.apiclient import ApiClient, PoodledoError, ToodledoError

from GT.dashboard import DashboardWidget

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

class TodoWidget(object):
    def do_login(self, credential_file):
        client = ApiClient()
        with open(os.path.expanduser(credential_file), "r") as f:
            auth = json.load(f)

        try:
            client.application_id = "dash"
            client.application_token = auth['app_token'].encode('rot13')
        except KeyError:
            raise PoodledoError("Application ID or token not specified in configuration")

        try:
            client._key = auth['session_key']
            client.getAccountInfo()
        except (ToodledoError, KeyError):
            # cached session key either wasn't there or wasn't good; get a new one and cache it
            client._key = None

            try:
                client.authenticate(auth['username'], auth['password'].encode('rot13'))
            except ToodledoError as e:
                print("No login credentials were successful; please try again.")
                raise e

            auth['session_key'] = client.key
            with open(os.path.expanduser(credential_file), "w") as f:
                json.dump(auth, f, indent=4)

        return client

    def render(self):
        credential_file = "~/.gt/dashboard.json"

        try:
            c = self.do_login(credential_file)
            todos = c.getTasks()
            todos.reverse()
            todos_list = list(dict(i) for i in todos)
        except urllib2.URLError:
            todos_list = []
        return todos_list[:40]
