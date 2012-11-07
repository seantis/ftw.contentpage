from zope.interface import Interface


class IContentPage(Interface):
    """Marker interface for ContenPages"""


class IAddressBlock(Interface):
    """Marker interface for AddressBlocks"""


class IAddressBlockView(Interface):
    """Marker interface for AddressBlocks"""


class IOrgUnitMarker(Interface):
    """Marker interface for AddressBlocks"""


class ICategorizable(Interface):
    """Marker interface for categorizable content"""
