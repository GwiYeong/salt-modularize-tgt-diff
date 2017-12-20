def _pki_minions(self):
    '''
    Retreive complete minion list from PKI dir.
    Respects cache if configured
    '''
    minions = []
    pki_cache_fn = os.path.join(self.opts['pki_dir'], self.acc, '.key_cache')
    try:
        if self.opts['key_cache'] and os.path.exists(pki_cache_fn):
            log.debug('Returning cached minion list')
            with salt.utils.files.fopen(pki_cache_fn) as fn_:
                return self.serial.load(fn_)
        else:
            for fn_ in salt.utils.data.sorted_ignorecase(os.listdir(os.path.join(self.opts['pki_dir'], self.acc))):
                if not fn_.startswith('.') and os.path.isfile(os.path.join(self.opts['pki_dir'], self.acc, fn_)):
                    minions.append(fn_)
        return minions
    except OSError as exc:
        log.error('Encountered OSError while evaluating  minions in PKI dir: {0}'.format(exc))
        return minions

