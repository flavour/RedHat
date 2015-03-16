# -*- coding: utf-8 -*-

from gluon import *
from s3 import S3CustomController

THEME = "RedHat"

# =============================================================================
class index(S3CustomController):
    """ Custom Home Page """

    def __call__(self):

        output = {}

        # Allow editing of page content from browser using CMS module
        if current.deployment_settings.has_module("cms"):
            system_roles = current.auth.get_system_roles()
            ADMIN = system_roles.ADMIN in current.session.s3.roles
            s3db = current.s3db
            table = s3db.cms_post
            ltable = s3db.cms_post_module
            module = "default"
            resource = "index"
            query = (ltable.module == module) & \
                    ((ltable.resource == None) | \
                     (ltable.resource == resource)) & \
                    (ltable.post_id == table.id) & \
                    (table.deleted != True)
            item = current.db(query).select(table.body,
                                            table.id,
                                            limitby=(0, 1)).first()
            if item:
                if ADMIN:
                    item = DIV(XML(item.body),
                               BR(),
                               A(current.T("Edit"),
                                 _href=URL(c="cms", f="post",
                                           args=[item.id, "update"]),
                                 _class="action-btn"))
                else:
                    item = DIV(XML(item.body))
            elif ADMIN:
                if current.response.s3.crud.formstyle == "bootstrap":
                    _class = "btn"
                else:
                    _class = "action-btn"
                item = A(current.T("Edit"),
                         _href=URL(c="cms", f="post", args="create",
                                   vars={"module": module,
                                         "resource": resource
                                         }),
                         _class="%s cms-edit" % _class)
            else:
                item = ""
        else:
            item = ""
        output["item"] = item

        self._view(THEME, "index.html")
        current.response.s3.stylesheets.append("../themes/CERT/homepage.css")
        
        T = current.T
        
        # @ToDo: Add event/human_resource - but this requires extending event_human_resource to link to event.
        menus = [{"title":T("Incidents"),
                  "icon":"bolt",
                  "description":T("Manage communication for specific incidents"),
                  "module":"deploy",
                  "function":"mission",
                  "buttons":[{"args":"summary",
                              "icon":"list",
                              "label":T("View"),
                             },
                             {"args":"create",
                              "icon":"plus-sign",
                              "label":T("Create"),
                             }]
                  },
                 {"title":T("Messaging"),
                  "icon":"envelope-alt",
                  "description":T("Send messages to individuals and groups"),
                  "module":"msg",
                  "function":"index",
                  "args":None,
                  "buttons":[{"function":"inbox",
                              "args":None,
                              "icon":"inbox",
                              "label":T("Inbox"),
                             },
                             {"function":"compose",
                              "args":None,
                              "icon":"plus-sign",
                              "label":T("Compose"),
                             }]
                  },
                 {"title":T("Staff"),
                  "icon":"group",
                  "description":T("The staff of your Organization and your partners"),
                  "module":"deploy",
                  "function":"human_resource",
                  "buttons":[{"args":"summary",
                              "icon":"list",
                              "label":T("View"),
                             },
                             {"args":"create",
                              "icon":"plus-sign",
                              "label":T("Create"),
                             }]
                  },
                 {"title":T("Offices"),
                  "icon":"building",
                  "description":T("Your and your partners' offices around the world"),
                  "module":"org",
                  "function":"office",
                  "buttons":[{"args":"summary",
                              "icon":"list",
                              "label":T("View"),
                             },
                             {"args":"create",
                              "icon":"plus-sign",
                              "label":T("Create"),
                             }]
                  },
                 ] 

        return dict(item = item,
                    menus=menus,
                    )

# END =========================================================================
