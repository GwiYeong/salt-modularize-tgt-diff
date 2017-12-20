def check_minions(expr, delimiter, greedy, pillar_exact=False):
    '''
    Return the minions found by looking via compound matcher
    '''
    return salt.tgt.check_compound_minions(__opts__, expr, delimiter, greedy, pillar_exact=pillar_exact)
