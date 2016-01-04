import smartsheet

#
# List All Contents
#

smart = smartsheet.Smartsheet()
contents = smart.Home.list_all_contents()
print(contents)
