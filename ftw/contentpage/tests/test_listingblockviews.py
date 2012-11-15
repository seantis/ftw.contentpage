from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.app.imaging.utils import getAllowedSizes
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from StringIO import StringIO
from unittest2 import TestCase
from zope.component import queryMultiAdapter
import os
import transaction



class TestListingBlockViews(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestListingBlockViews, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()
        transaction.commit()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def _create_listingblock(self):
        listingblock = self.contentpage.get(
            self.contentpage.invokeFactory('ListingBlock', 'listingblock'))
        # Fire all necessary events
        listingblock.processForm()
        transaction.commit()
        return listingblock

    def test_listing_view_registration(self):
        listingblock = self._create_listingblock()
        view = queryMultiAdapter((listingblock, listingblock.REQUEST),
                                 name="block_view")
        self.assertNotEquals(view, None)

    def test_gallery_view_registration(self):
        listingblock = self._create_listingblock()
        view = queryMultiAdapter((listingblock, listingblock.REQUEST),
                                 name="block_view-gallery")
        self.assertNotEquals(view, None)

    def test_listingblock_view(self):
        listingblock = self._create_listingblock()
        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        self.assertIn(listingblock.getId(), self.browser.contents)
        self.assertIn('simplelayout-block-wrapper ListingBlock',
                      self.browser.contents)

    def test_listing_block_table_render(self):
        listingblock = self._create_listingblock()
        _file = listingblock.get(
            listingblock.invokeFactory('File', 'file'))
        dummy = StringIO("DATA")
        dummy.filename = 'dummy.pdf'
        _file.setFile(dummy)
        _file.setTitle("Dummy PDF")
        _file.processForm()

        view = queryMultiAdapter((listingblock, listingblock.REQUEST),
                                 name='block_view')
        self.assertIn("Dummy PDF", view.render_table())
        self.assertIn("pdf.png", view.render_table())

    def test_scale_installed(self):
        listingblock = self._create_listingblock()
        _image = listingblock.get(
            listingblock.invokeFactory('Image', 'image'))
        scales = _image.restrictedTraverse('@@images')
        self.assertIn('listingblock_gallery', scales.getAvailableSizes())

    def test_gallery_get_box_boundaries(self):
        listingblock = self._create_listingblock()
        view = queryMultiAdapter((listingblock, listingblock.REQUEST),
                         name='block_view-gallery')
        self.assertEquals(getAllowedSizes()['listingblock_gallery'],
            view._get_box_boundaries())

    def test_gallery_get_images(self):
        listingblock = self._create_listingblock()
        _image = (listingblock.get(
            listingblock.invokeFactory('Image', 'image')))
        listingblock.invokeFactory('File', 'file')
        view = queryMultiAdapter((listingblock, listingblock.REQUEST),
                         name='block_view-gallery')
        #Only return images
        self.assertEquals([_image], view.get_images())

    def test_gallery_view(self):
        listingblock = self._create_listingblock()
        _image = listingblock.get(
            listingblock.invokeFactory('Image', 'image'))

        dummy = open("%s/dummy.png" % os.path.split(__file__)[0], 'r')
        dummy.seek(0)
        _image.setImage(dummy)
        _image.setTitle('Dummy Image')
        _image.processForm()

        view = queryMultiAdapter((listingblock, listingblock.REQUEST),
                                 name='block_view-gallery')
        self.assertIn("<img src=\"http://nohost/plone/contentpage/"
            "listingblock/image/@@images",
                      view.index())
        self.assertIn("title=\"Dummy Image\"", view.index())

    def tearDown(self):
        super(TestListingBlockViews, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage'])

        transaction.commit()