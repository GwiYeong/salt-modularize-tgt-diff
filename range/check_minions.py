def check_minions(expr, greedy):
    '''
    Return the minions found by looking via range expression
    '''
    if not HAS_RANGE:
        raise CommandExecutionError(
            'Range matcher unavailable (unable to import seco.range, '
            'module most likely not installed)'
        )
    _range = seco.range.Range(__opts__['range_server'])
    try:
        return _range.expand(expr)
    except seco.range.RangeException as exc:
        log.error(
            'Range exception in compound match: {0}'.format(exc)
        )
        cache_enabled = __opts__.get('minion_data_cache', False)
        if greedy:
            mlist = salt.tgt.pki_dir_minions(__opts__)
            return {'minions': mlist,
                    'missing': []}
        elif cache_enabled:
            cache = salt.cache.factory(__opts__)
            return {'minions': cache.list('minions'),
                    'missing': []}
        else:
            return {'minions': [],
                    'missing': []}
