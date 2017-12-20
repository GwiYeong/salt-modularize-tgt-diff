def fill_auth_list_from_groups(self, auth_provider, user_groups, auth_list):
    '''
    Returns a list of authorisation matchers that a user is eligible for.
    This list is a combination of the provided personal matchers plus the
    matchers of any group the user is in.
    '''
    group_names = [item for item in auth_provider if item.endswith('%')]
    if group_names:
        for group_name in group_names:
            if group_name.rstrip("%") in user_groups:
                for matcher in auth_provider[group_name]:
                    auth_list.append(matcher)
    return auth_list

