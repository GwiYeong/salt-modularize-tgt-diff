def mine_get(tgt, fun, tgt_type='glob', opts=None):
    '''
    Gathers the data from the specified minions' mine, pass in the target,
    function to look up and the target type
    '''
    ret = {}
    _res = check_minions(opts, tgt, tgt_type)
    minions = _res['minions']
    cache = salt.cache.factory(opts)
    for minion in minions:
        mdata = cache.fetch('minions/{0}'.format(minion), 'mine')
        if mdata is None:
            continue
        fdata = mdata.get(fun)
        if fdata:
            ret[minion] = fdata
    return ret
