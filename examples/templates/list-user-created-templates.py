from pprint import pprint
import smartsheet

#
# List all user created templates the current user may access.
#

smart = smartsheet.Smartsheet()
action = smart.Templates.list_user_created_templates(include_all=True)
templates = [(x.to_dict() if hasattr(x, 'to_dict') else x) for x in action.result]

pprint(templates)

print(action.requests_response.status_code)