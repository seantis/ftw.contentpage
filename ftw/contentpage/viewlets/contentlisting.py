from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize import instance


class ContentListingViewlet(ViewletBase):
    """Lists content by categories"""
    render = ViewPageTemplateFile('contentlisting.pt')

    def available(self):
        return bool(self.get_content())

    @instance.memoize
    def get_content(self):
        query = {'portal_type': 'ContentPage'}
        contents = self.context.getFolderContents(contentFilter=query,
                                                  full_objects=True)
        return self._create_resultmap(contents)

    def _create_resultmap(self, contents=[]):
        resultmap = {}
        for obj in contents:
            categories = obj.Schema()['categories'].get(obj)

            for cat in categories:
                if cat not in resultmap:
                    resultmap[cat] = []
                resultmap[cat].append((obj.title_or_id(),
                                       obj.absolute_url(), ))

        for value in resultmap.values():
            value.sort()
        # Return result sorted by title_or_id
        return sorted(resultmap.items(), key=lambda item: item[1][0])