def check_cache_minions(opts,
                        expr,
                        delimiter,
                        greedy,
                        search_type,
                        regex_match=False,
                        exact_match=False):
    '''
    Helper function to search for minions in master caches
    If 'greedy' return accepted minions that matched by the condition or absend in the cache.
    If not 'greedy' return the only minions have cache data and matched by the condition.
    '''
    cache = salt.cache.factory(opts)
    cache_enabled = opts.get('minion_data_cache', False)

    def list_cached_minions():
        return cache.list('minions')

    if greedy:
        minions = pki_dir_minions(opts)
    elif cache_enabled:
        minions = list_cached_minions()
    else:
        return {'minions': [],
                'missing': []}

    if cache_enabled:
        if greedy:
            cminions = list_cached_minions()
        else:
            cminions = minions
        if not cminions:
            return {'minions': minions,
                    'missing': []}
        minions = set(minions)
        for id_ in cminions:
            if greedy and id_ not in minions:
                continue
            mdata = cache.fetch('minions/{0}'.format(id_), 'data')
            if mdata is None:
                if not greedy:
                    minions.remove(id_)
                continue
            search_results = mdata.get(search_type)
            if not salt.utils.data.subdict_match(search_results,
                                                 expr,
                                                 delimiter=delimiter,
                                                 regex_match=regex_match,
                                                 exact_match=exact_match):
                minions.remove(id_)
        minions = list(minions)
    return {'minions': minions,
            'missing': []}


