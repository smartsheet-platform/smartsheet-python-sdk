from pprint import pprint
import smartsheet

#
# List all Sheets.
#

smart = smartsheet.Smartsheet()
action = smart.Templates.list_public_templates(include_all=True)
templates = [(x.to_dict() if hasattr(x, 'to_dict') else x) for x in action.result]

pprint(templates)
