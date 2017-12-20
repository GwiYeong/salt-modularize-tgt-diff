def check_minions(opts,
                  expr,
                  tgt_type='glob',
                  delimiter=DEFAULT_TARGET_DELIM,
                  greedy=True):
    '''
    Check the passed regex against the available minions' public keys
    stored for authentication. This should return a set of ids which
    match the regex, this will then be used to parse the returns to
    Make sure everyone has checked back in.
    '''
    tgts = salt.loader.tgt(opts)
    if expr is None:
        expr = ''
    fstr = '{0}.check_minions'.format(tgt_type)
    if fstr not in tgts:
        log.warn('Failed to find function for matching minion '
                 'with given tgt_type : {0}, fstr: {1}'
                 .format(tgt_type, fstr))
        return {'minions': [], 'missing': []}

    try:
        fcall = salt.utils.args.format_call(tgts[fstr],
                                            {'expr': expr, 'delimiter': delimiter, 'greedy': greedy})
        return tgts[fstr](*fcall['args'], **fcall.get('kwargs', {}))
    except Exception as e:
        log.error(('Failed to match available minions with tgt_type: {0} pattern: {1}'
                   .format(tgt_type, expr)))
        return {'minions': [], 'missing': []}


