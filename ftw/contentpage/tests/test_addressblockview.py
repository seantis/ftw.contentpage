from ftw.contentpage.testing import ZCML_LAYER
from ftw.testing import MockTestCase
from zope.component import getMultiAdapter
from ftw.contentpage.interfaces import IAddressBlock
from mocker import ANY

OPENING_HOURS = "Line1\nLine2\nLine3"


class TestAddressBlockView(MockTestCase):

    layer = ZCML_LAYER

    def setUp(self):
        super(TestAddressBlockView, self).setUp()

        self.request = self.stub_request()
        self.context = self.providing_stub(IAddressBlock)
        self.expect(self.context.getAddress()).result("Address line")
        self.expect(self.context.getOpeningHours()).result(OPENING_HOURS)
        self.expect(self.context.getExtraAddressLine()).result(
            "Additional line")

    def test_component_registered_view(self):
        self.replay()
        self.assertNotEquals(getMultiAdapter(
            (self.context, self.request), name="block_view"),
            None)

    def test_component_registered_portlet_view(self):
        self.replay()
        self.assertNotEquals(getMultiAdapter(
            (self.context, self.request), name="block_view-portlet"),
            None)

    def test_get_address_as_html(self):
        self.replay()
        view = getMultiAdapter((self.context, self.request),
                               name="block_view")
        self.assertEquals(view.get_address_as_html(),
                          "Address line<br />Additional line")

    def test_get_opening_hours_as_html(self):
        self.replay()
        view = getMultiAdapter((self.context, self.request),
                               name="block_view")
        self.assertEquals(view.get_opening_hours_as_html(),
                          "Line1<br />Line2<br />Line3")

    def test_has_team(self):
        self.context.aq_parent = self.mocker.mock(count=False)
        self.expect(self.context.aq_parent.getFolderContents(ANY)).result(True)
        self.replay()
        view = getMultiAdapter(
            (self.context, self.request), name="block_view-portlet")
        view.has_team

    def test_has_no_team(self):
        self.context.aq_parent = self.mocker.mock(count=False)
        self.expect(self.context.aq_parent.getFolderContents(ANY)).result(
            False)
        self.replay()
        view = getMultiAdapter(
            (self.context, self.request), name="block_view-portlet")
        view.has_team

