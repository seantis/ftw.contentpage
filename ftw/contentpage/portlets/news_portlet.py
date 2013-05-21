from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.contentpage import _
from ftw.contentpage.portlets import base as base_portlet
from zope.interface import implements


class INewsPortlet(base_portlet.IBasePortlet):
    """Dataprovider"""


class AddForm(base_portlet.AddForm):
    label = _(u'Add News Portlet')
    description = _(u'This Portlet displays News')

    def create(self, data):
        return Assignment(
            portlet_title=data.get('portlet_title', 'News'),
            show_image=data.get('show_image', True),
            only_context=data.get('only_context', True),
            quantity=data.get('quantity', 5),
            classification_items=data.get('classification_items', []),
            path=data.get('path', []),
            subjects=data.get('subjects', []),
            show_desc=data.get('show_desc', False),
            desc_length=data.get('desc_length', 50),
            days=data.get('days', 0),
            more_news_link=data.get('more_news_link', 0)
        )


class Assignment(base_portlet.Assignment):
    implements(INewsPortlet)

    @property
    def title(self):
        return u'News Portlet'


class Renderer(base_portlet.Renderer):
    render = ViewPageTemplateFile('news_portlet.pt')

    @property
    def available(self):
        is_news = self.context.portal_type in ['News', 'NewsFolder']
        if self.show_more_news_link():
            has_news = self.get_news(all_news=True)
        else:
            has_news = self.get_news()
        return has_news and not is_news

    def get_items(self, all_items=False):
        return super(Renderer, self).get_items("News",
                                               "effective",
                                               "descending",
                                               all_items=all_items)


class EditForm(base_portlet.EditForm):
    label = _(u'Add News Portlet')
    description = _(u'This Portlet displays News')
