# -*- coding: utf-8 -*-
import requests
import lxml.html

__all__ = 'Dictionary', 'get_dictionary'

class Dictionary(object):

    _origin = ''
    _translate = ''

    def __init__(self, name, url):
        self.url = url
        self.name = name

    def get_meaning_from_url(self):
        raise NotImplementedError('`get_meaning_from_url` MUST implemented.')

    def translate(self, word):
        self._origin = word
        self._translate = self.get_meaning_from_url()
        return self.get_meaning_from_url()


def get_dictionary(**options):
    def f(self):
        r = requests.get(self.url.format(self._origin))
        result = ''
        if (r.status_code == 200 and
               r.headers['content-type'].startswith('text/html')):
            html = lxml.html.fromstring(r.text)
            finds = []
            if isinstance(options['path'], basestring):
                finds = html.xpath(options['path'])
            elif isinstance(options['path'], list):
                for p in options['path']:
                    finds = html.xpath(p)
                    if len(finds):
                        break

            results = [f.text_content().strip() for f in finds]
            result = ', '.join(results)
        else:
            print('status: {0} returned in url={1}'.format(r.status_code,
                                                           self.url))
        return result

    MetaTranslator = type('Dictionary', (), dict(Dictionary.__dict__))
    setattr(MetaTranslator, 'get_meaning_from_url', f)

    return MetaTranslator(options['name'], options['url'])
