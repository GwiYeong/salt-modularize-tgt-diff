def fill_auth_list(self, auth_provider, name, groups, auth_list=None, permissive=None):
    '''
    Returns a list of authorisation matchers that a user is eligible for.
    This list is a combination of the provided personal matchers plus the
    matchers of any group the user is in.
    '''
    if auth_list is None:
        auth_list = []
    if permissive is None:
        permissive = self.opts.get('permissive_acl')
    name_matched = False
    for match in auth_provider:
        if match == '*' and not permissive:
            continue
        if match.endswith('%'):
            if match.rstrip('%') in groups:
                auth_list.extend(auth_provider[match])
        else:
            if salt.utils.stringutils.expr_match(match, name):
                name_matched = True
                auth_list.extend(auth_provider[match])
    if not permissive and not name_matched and '*' in auth_provider:
        auth_list.extend(auth_provider['*'])
    return auth_list

