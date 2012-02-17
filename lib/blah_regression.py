import re

'''
Implemented methods enumeration:
1)  check_error_for_bug_84261


'''

def check_error_for_bug_84261(err_to_check):
    '''

    '''

    ret_val = ['SUCCESS', 'FAILURE']
    if len(err_to_check) != 0:
        if re.search("/usr/bin/BNotifier: Error creating and binding socket: Address already in use",  err_to_check):
            return ret_val[1]
        else:
            return ret_val[0]
    else:
        ret_val[0]

