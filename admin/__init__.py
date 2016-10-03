from flask_admin.contrib.pymongo import ModelView, filters
from wtforms import form, fields
from datetime import datetime
from slugify import slugify


class SubmitForm(form.Form):
    author = fields.StringField('Author')
    title = fields.StringField('Title')
    subtitle = fields.StringField('Sub-Title')
    body = fields.TextAreaField('Post')
    year_month = fields.HiddenField('year_month', default=datetime.utcnow().strftime("%Y%m"))
    timestamp = fields.HiddenField('timestamp', default=datetime.utcnow().strftime("%A %x"))


class PostView(ModelView):
    column_list = ('Author', 'Title', 'Sub-Title', 'Post')

    form = SubmitForm

    def get_list(self, *args, **kwargs):
        count, data = super(PostView, self).get_list(*args, **kwargs)

        post_cutoff = 40
        for item in data:
            item['Author'] = item['author']
            item['Title'] = item['title']
            item['Sub-Title'] = item['subtitle']

            post = item['body']
            if len(post) >= post_cutoff:
                post = post[:post_cutoff] + '...'
            item['Post'] = post

        return count, data

    def on_model_change(self, form, model, is_created):
        """
        Create 'url_slug' form 'title'
        """
        model['url_slug'] = slugify(model['title'])
