def check_minions(self,
                  expr,
                  tgt_type='glob',
                  delimiter=DEFAULT_TARGET_DELIM,
                  greedy=True):
    '''
    Check the passed regex against the available minions' public keys
    stored for authentication. This should return a set of ids which
    match the regex, this will then be used to parse the returns to
    make sure everyone has checked back in.
    '''

    try:
        if expr is None:
            expr = ''
        check_func = getattr(self, '_check_{0}_minions'.format(tgt_type), None)
        if tgt_type in ('grain',
                         'grain_pcre',
                         'pillar',
                         'pillar_pcre',
                         'pillar_exact',
                         'compound',
                         'compound_pillar_exact'):
            _res = check_func(expr, delimiter, greedy)
        else:
            _res = check_func(expr, greedy)
    except Exception:
        log.exception(
                'Failed matching available minions with {0} pattern: {1}'
                .format(tgt_type, expr))
        _res = {'minions': [], 'missing': []}
    return _res

