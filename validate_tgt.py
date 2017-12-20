def validate_tgt(opts, valid, expr, tgt_type, minions=None, expr_form=None):
    '''
    Return a Bool. This function returns if the expression sent in is
    within the scope of the valid expression
    '''
    # remember to remove the expr_form argument from this function when
    # performing the cleanup on this deprecation.
    if expr_form is not None:
        salt.utils.versions.warn_until(
            'Fluorine',
            'the target type should be passed using the \'tgt_type\' '
            'argument instead of \'expr_form\'. Support for using '
            '\'expr_form\' will be removed in Salt Fluorine.'
        )
        tgt_type = expr_form

    v_minions = _expand_matching(opts, valid)
    if minions is None:
        _res = check_minions(opts, expr, tgt_type)
        minions = set(_res['minions'])
    else:
        minions = set(minions)
    d_bool = not bool(minions.difference(v_minions))
    if len(v_minions) == len(minions) and d_bool:
        return True
    return d_bool

