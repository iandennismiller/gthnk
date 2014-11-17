# (c) 2013 www.turkr.com

import json
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.security import current_user
from Gthnk import Models, security

import flask

class EntryExplorer(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()

    can_create = False
    can_delete = False
    can_edit = False
    column_list=["timestamp", "content"]
    #column_filters = ['source', 'timestamp', 'author', 'title']
    column_sortable_list = (('timestamp', 'timestamp'))
    column_searchable_list = ['content']

    #list_template = 'explorer/article_list.html'

    @expose("/comment/")
    def comment_view(self):
        c_id = flask.request.args['id']
        if c_id is None:
            return flask.redirect(url_for('admin.index'))

        comment = Models.Comment.query.get(c_id)
        return self.render('explorer/comment_view.html',comment=comment,
            liwc_json=json.dumps(comment.liwc.as_hash(), sort_keys=True, indent=4))

        #return flask.render_template('explorer/comment_view.html',comment=comment,
        #    liwc_json=json.dumps(comment.liwc.as_hash(), sort_keys=True, indent=4))

    @expose("/article/")
    def article_view(self):
        a_id = flask.request.args['id']
        if a_id is None:
            return flask.redirect(url_for('admin.index'))

        article = Models.Article.query.get(a_id)
        listing_count = Models.Listing.query.filter_by(article=article).count()
        return self.render('explorer/article_view.html',article=article, listing_count=listing_count,
            liwc_json=json.dumps(article.liwc.as_hash(), sort_keys=True, indent=4))

    def __init__(self, session, **kwds):
        super(EntryExplorer, self).__init__(Models.Entry, session, **kwds)
