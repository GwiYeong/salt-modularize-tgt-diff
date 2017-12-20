def get_minion_data(minion, opts):
    '''
    Get the grains/pillar for a specific minion.  If minion is None, it
    will return the grains/pillar for the first minion it finds.

    Return value is a tuple of the minion ID, grains, and pillar
    '''
    grains = None
    pillar = None
    if opts.get('minion_data_cache', False):
        cache = salt.cache.factory(opts)
        if minion is None:
            for id_ in cache.list('minions'):
                data = cache.fetch('minions/{0}'.format(id_), 'data')
                if data is None:
                    continue
        else:
            data = cache.fetch('minions/{0}'.format(minion), 'data')
        if data is not None:
            grains = data.get('grains', None)
            pillar = data.get('pillar', None)
    return minion if minion else None, grains, pillar


