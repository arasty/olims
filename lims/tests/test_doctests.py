from lims.testing import BIKA_FUNCTIONAL_TESTING
from dependencies.dependency import DocFileSuite
from dependencies.dependency import DocTestSuite
from dependencies.dependency import layered
import doctest
import unittest

OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

DOCTESTS = [
    'bika.lims.browser.accreditation',
    'bika.lims.browser.analysisrequest.add',
    'bika.lims.browser.bika_listing',
    'bika.lims.browser.instrument',
    'bika.lims.jsonapi.create',
    'bika.lims.jsonapi.update',
	'bika.lims.jsonapi.remove',
    'bika.lims.vocabularies',
]


def test_suite():
    suite = unittest.TestSuite()
    for module in DOCTESTS:
        suite.addTests([
            layered(DocTestSuite(module=module, optionflags=OPTIONFLAGS),
                    layer=BIKA_FUNCTIONAL_TESTING),
        ])
    return suite
