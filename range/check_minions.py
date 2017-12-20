def _check_range_minions(self, expr, greedy):
    '''
    Return the minions found by looking via range expression
    '''
    if not HAS_RANGE:
        raise CommandExecutionError(
            'Range matcher unavailable (unable to import seco.range, '
            'module most likely not installed)'
        )
    if not hasattr(self, '_range'):
        self._range = seco.range.Range(self.opts['range_server'])
    try:
        return self._range.expand(expr)
    except seco.range.RangeException as exc:
        log.error(
            'Range exception in compound match: {0}'.format(exc)
        )
        cache_enabled = self.opts.get('minion_data_cache', False)
        if greedy:
            mlist = []
            for fn_ in salt.utils.data.sorted_ignorecase(os.listdir(os.path.join(self.opts['pki_dir'], self.acc))):
                if not fn_.startswith('.') and os.path.isfile(os.path.join(self.opts['pki_dir'], self.acc, fn_)):
                    mlist.append(fn_)
            return {'minions': mlist,
                    'missing': []}
        elif cache_enabled:
            return {'minions': self.cache.list('minions'),
                    'missing': []}
        else:
            return {'minions': [],
                    'missing': []}

