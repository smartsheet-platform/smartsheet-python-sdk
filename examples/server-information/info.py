from pprint import pprint
import smartsheet

smart = smartsheet.Smartsheet()
info = smart.Server.server_info()

pprint(info.to_dict())