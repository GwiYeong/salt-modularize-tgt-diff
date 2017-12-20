def _args_check(valid, args=None, kwargs=None):
    '''
    valid is a dicts: {'args': [...], 'kwargs': {...}} or a list of such dicts.
    '''
    if not isinstance(valid, list):
        valid = [valid]
    for cond in valid:
        if not isinstance(cond, dict):
            # Invalid argument
            continue
        # whitelist args, kwargs
        cond_args = cond.get('args', [])
        good = True
        for i, cond_arg in enumerate(cond_args):
            if args is None or len(args) <= i:
                good = False
                break
            if cond_arg is None:  # None == '.*' i.e. allow any
                continue
            if not _match_check(cond_arg, str(args[i])):
                good = False
                break
        if not good:
            continue
        # Check kwargs
        cond_kwargs = cond.get('kwargs', {})
        for k, v in six.iteritems(cond_kwargs):
            if kwargs is None or k not in kwargs:
                good = False
                break
            if v is None:  # None == '.*' i.e. allow any
                continue
            if not _match_check(v, str(kwargs[k])):
                good = False
                break
        if good:
            return True
    return False


