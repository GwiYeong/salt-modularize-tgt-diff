def check_minions(expr):
    '''
    Return the minions found by looking via globs
    '''
    pki_minions = salt.tgt.pki_minions(__opts__)
    return {'minions': fnmatch.filter(pki_minions, expr), 'missing': []}
