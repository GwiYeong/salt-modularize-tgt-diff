def wheel_check(self, auth_list, fun, args):
    '''
    Check special API permissions
    '''
    return self.spec_check(auth_list, fun, args, 'wheel')

