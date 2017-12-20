def wheel_check(auth_list, fun, args):
    '''
    Check special API permissions
    '''
    return spec_check(auth_list, fun, args, 'wheel')

