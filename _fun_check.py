def _fun_check(valid, fun, args=None, kwargs=None):
    '''
    Check the given function name (fun) and its arguments (args) against the list of conditions.
    '''
    if not isinstance(valid, list):
        valid = [valid]
    for cond in valid:
        # Function name match
        if isinstance(cond, six.string_types):
            if _match_check(cond, fun):
                return True
        # Function and args match
        elif isinstance(cond, dict):
            if len(cond) != 1:
                # Invalid argument
                continue
            fname_cond = next(six.iterkeys(cond))
            if _match_check(fname_cond, fun):  # check key that is function name match
                if _args_check(cond[fname_cond], args, kwargs):
                    return True
    return False

