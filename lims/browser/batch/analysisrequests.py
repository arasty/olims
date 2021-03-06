from operator import itemgetter
from lims import bikaMessageFactory as _
from lims.utils import t
from lims.browser.analysisrequest import AnalysisRequestAddView as _ARAV
from lims.browser.analysisrequest import AnalysisRequestsView as _ARV
from lims.permissions import *
from dependencies.dependency import IViewView
from dependencies.dependency import getToolByName
from dependencies.dependency import ViewPageTemplateFile
from dependencies.dependency import implements


class AnalysisRequestsView(_ARV, _ARAV):
    template = ViewPageTemplateFile(
        "../analysisrequest/templates/analysisrequests.pt")
    ar_add = ViewPageTemplateFile("../analysisrequest/templates/ar_add.pt")
    implements(IViewView)

    def __init__(self, context, request):
        super(AnalysisRequestsView, self).__init__(context, request)

    def contentsMethod(self, contentFilter):
        #bc = getToolByName(self.context, 'bika_catalog')
        #import pdb;pdb.set_trace()
        #if 'BatchUID' not in contentFilter.keys():
        #    contentFilter['BatchUID'] = self.context.UID()
        #return bc(contentFilter)
        return self.context.getBackReferences("AnalysisRequestBatch")

    def __call__(self):
        self.context_actions = {}
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.checkPermission(AddAnalysisRequest, self.portal):
            self.context_actions[self.context.translate(_('Add new'))] = {
                'url': self.context.absolute_url() + \
                    "/portal_factory/"
                    "AnalysisRequest/Request new analyses/ar_add?ar_count=1",
                'icon': '++resource++bika.lims.images/add.png'}

        return super(AnalysisRequestsView, self).__call__()

    def getMemberDiscountApplies(self):
        client = self.context.getClient()
        return client and client.getMemberDiscountApplies() or False

    def getRestrictedCategories(self):
        client = self.context.getClient()
        return client and client.getRestrictedCategories() or []

    def getDefaultCategories(self):
        client = self.context.getClient()
        return client and client.getDefaultCategories() or []
