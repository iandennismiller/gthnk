import re
import jinja2

###
# Slugify: https://gist.github.com/berlotto/6295018

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    
    From Django's "django/template/defaultfilters.py".
    """
    # import unicodedata
    # if not isinstance(value, unicode):
    #     value = unicode(value)
    # value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    
    value = _slugify_strip_re.sub('', value).strip().lower()

    return _slugify_hyphenate_re.sub('-', value)

@jinja2.contextfilter
def _slugify(string):
    if not string:
        return ""
    return slugify(string)
