# -*- coding: utf-8 -*-
# gthnk (c) Ian Dennis Miller

import sublime
import sublime_plugin
import datetime


def scroll_to_end(self):
    (row, col) = self.view.rowcol(1000000)
    pt = self.view.text_point(row, 0)

    self.view.sel().clear()
    self.view.sel().add(sublime.Region(pt))
    self.view.show(pt)


class insert_date(sublime_plugin.TextCommand):
    """Add the next occurrence of the word under the cursor to the selection"""

    def run(self, edit):
        scroll_to_end(self)
        n = datetime.datetime.now()
        stamp = "%s-%0.2d-%0.2d\n\n" % (n.year, int(n.month), int(n.day))
        self.view.insert(edit, self.view.sel()[0].end(), stamp)


class insert_time(sublime_plugin.TextCommand):
    """Add the next occurrence of the word under the cursor to the selection"""

    def run(self, edit):
        scroll_to_end(self)

        n = datetime.datetime.now()
        stamp = "%0.2d%0.2d\n\n" % (int(n.hour), int(n.minute))
        self.view.insert(edit, self.view.sel()[0].end(), stamp)
        self.view.run_command("save")
