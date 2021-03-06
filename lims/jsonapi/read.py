from dependencies.dependency import safe_unicode
from lims import logger, to_utf8
from lims.interfaces import IJSONReadExtender
from lims.jsonapi import get_include_fields
from dependencies.dependency import router
from dependencies.dependency import IRouteProvider
from dependencies.dependency import AuthenticatorView
from lims.jsonapi import load_brain_metadata
from lims.jsonapi import load_field_values
from dependencies.dependency import getToolByName
from dependencies.dependency import interface
from dependencies.dependency import getAdapters
import re
# import App #Plone/buildout-cache/eggs/Zope2-2.13.22-py2.7.egg/App


def read(context, request):
    tag = AuthenticatorView(context, request).authenticator()
    pattern = '<input .*name="(\w+)".*value="(\w+)"'
    _authenticator = re.match(pattern, tag).groups()[1]

    ret = {
        "url": router.url_for("read", force_external=True),
        "success": True,
        "error": False,
        "objects": [],
        "_authenticator": _authenticator,
    }
    debug_mode = True #App.config.getConfiguration().debug_mode "Commented by Yasir"
    catalog_name = request.get("catalog_name", "portal_catalog")
    if not catalog_name:
        raise ValueError("bad or missing catalog_name: " + catalog_name)
    catalog = getToolByName(context, catalog_name)
    indexes = catalog.indexes()

    contentFilter = {}
    for index in indexes:
        if index in request:
            if index == 'review_state' and "{" in request[index]:
                continue
            contentFilter[index] = safe_unicode(request[index])
        if "%s[]"%index in request:
            value = request["%s[]"%index]
            contentFilter[index] = [safe_unicode(v) for v in value]

    if 'limit' in request:
        try:
            contentFilter['sort_limit'] = int(request["limit"])
        except ValueError:
            pass
    sort_on = request.get('sort_on', 'id')
    contentFilter['sort_on'] = sort_on
    # sort order
    sort_order = request.get('sort_order', '')
    if sort_order:
        contentFilter['sort_order'] = sort_order
    else:
        sort_order = 'ascending'
        contentFilter['sort_order'] = 'ascending'

    include_fields = get_include_fields(request)
    if debug_mode:
        logger.info("contentFilter: " + str(contentFilter))

    # Get matching objects from catalog
    proxies = catalog(**contentFilter)

    # batching items
    page_nr = int(request.get("page_nr", 0))
    try:
        page_size = int(request.get("page_size", 10))
    except ValueError:
        page_size = 10
    # page_size == 0: show all
    if page_size == 0:
        page_size = len(proxies)
    first_item_nr = page_size * page_nr
    if first_item_nr > len(proxies):
        first_item_nr = 0
    page_proxies = proxies[first_item_nr:first_item_nr + page_size]
    for proxy in page_proxies:
        obj_data = {}

        # Place all proxy attributes into the result.
        obj_data.update(load_brain_metadata(proxy, include_fields))

        # Place all schema fields ino the result.
        obj = proxy.getObject()
        obj_data.update(load_field_values(obj, include_fields))

        obj_data['path'] = "/".join(obj.getPhysicalPath())

        # call any adapters that care to modify this data.
        adapters = getAdapters((obj, ), IJSONReadExtender)
        for name, adapter in adapters:
            adapter(request, obj_data)

        ret['objects'].append(obj_data)

    ret['total_objects'] = len(proxies)
    ret['first_object_nr'] = first_item_nr
    last_object_nr = first_item_nr + len(page_proxies)
    if last_object_nr > ret['total_objects']:
        last_object_nr = ret['total_objects']
    ret['last_object_nr'] = last_object_nr

    if debug_mode:
        logger.info("{0} objects returned".format(len(ret['objects'])))
    return ret


class Read(object):
    interface.implements(IRouteProvider)

    def initialize(self, context, request):
        pass

    @property
    def routes(self):
        return (
            ("/read", "read", self.read, dict(methods=['GET', 'POST'])),
        )

    def read(self, context, request):
        """/@@API/read: Search the catalog and return data for all objects found

        Optional parameters:

            - catalog_name: uses portal_catalog if unspecified
            - limit  default=1
            - All catalog indexes are searched for in the request.

        {
            runtime: Function running time.
            error: true or string(message) if error. false if no error.
            success: true or string(message) if success. false if no success.
            objects: list of dictionaries, containing catalog metadata
        }
        """

        return read(context, request)
