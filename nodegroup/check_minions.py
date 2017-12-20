def check_minions(expr, greedy):
    '''
    Return minions found by looking at nodegroups
    '''
    return salt.tgt.check_compound_minions(__opts__,
                                           salt.tgt.nodegroup_comp(expr, __opts__['nodegroups']),
                                           DEFAULT_TARGET_DELIM,
                                           greedy)
