def check_minions(expr):
    '''
    Return the minions found by looking via regular expressions
    '''
    pki_minions = salt.tgt.pki_minions(__opts__)
    reg = re.compile(expr)
    return {'minions': [m for m in pki_minions if reg.match(m)],
            'missing': []}
