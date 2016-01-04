import smartsheet

smart = smartsheet.Smartsheet()
me = smart.Users.get_current_user()
print(me)
