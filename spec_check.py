def spec_check(auth_list, fun, args, form):
    '''
    Check special API permissions
    '''
    if not auth_list:
        return False
    if form != 'cloud':
        comps = fun.split('.')
        if len(comps) != 2:
            # Hint at a syntax error when command is passed improperly,
            # rather than returning an authentication error of some kind.
            # See Issue #21969 for more information.
            return {'error': {'name': 'SaltInvocationError',
                              'message': 'A command invocation error occurred: Check syntax.'}}
        mod_name = comps[0]
        fun_name = comps[1]
    else:
        fun_name = mod_name = fun
    for ind in auth_list:
        if isinstance(ind, six.string_types):
            if ind[0] == '@':
                if ind[1:] == mod_name or ind[1:] == form or ind == '@{0}s'.format(form):
                    return True
        elif isinstance(ind, dict):
            if len(ind) != 1:
                continue
            valid = next(six.iterkeys(ind))
            if valid[0] == '@':
                if valid[1:] == mod_name:
                    if _fun_check(ind[valid], fun_name, args.get('arg'), args.get('kwarg')):
                        return True
                if valid[1:] == form or valid == '@{0}s'.format(form):
                    if _fun_check(ind[valid], fun, args.get('arg'), args.get('kwarg')):
                        return True
    return False

