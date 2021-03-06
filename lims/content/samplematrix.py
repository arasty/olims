from dependencies.dependency import ClassSecurityInfo
from dependencies.dependency import *
from dependencies.dependency import HoldingReference
from dependencies.dependency import RecordsField as RecordsField
from dependencies.dependency import getToolByName
from lims.browser.widgets import RecordsWidget
from lims.content.bikaschema import BikaSchema
from lims.config import PROJECTNAME
import sys
from lims import bikaMessageFactory as _
from lims.utils import t
from dependencies.dependency import implements

schema = BikaSchema.copy() + Schema((

))

schema['description'].schemata = 'default'
schema['description'].widget.visible = True

class SampleMatrix(BaseFolder):
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

registerType(SampleMatrix, PROJECTNAME)

def SampleMatrices(self, instance=None, allow_blank=False):
    instance = instance or self
    bsc = getToolByName(instance, 'bika_setup_catalog')
    items = []
    for sm in bsc(portal_type='SampleMatrix',
                  inactive_state='active',
                  sort_on = 'sortable_title'):
        items.append((sm.UID, sm.Title))
    items = allow_blank and [['','']] + list(items) or list(items)
    return DisplayList(items)
