def pki_minions(opts):
    '''
    Retreive complete minion list from PKI dir.
    Respects cache if configured
    '''
    acc = pki_dir_acc_path(opts)
    serial = salt.payload.Serial(opts)
    minions = []
    pki_cache_fn = os.path.join(opts['pki_dir'], acc, '.key_cache')
    try:
        if opts['key_cache'] and os.path.exists(pki_cache_fn):
            log.debug('Returning cached minion list')
            with salt.utils.files.fopen(pki_cache_fn) as fn_:
                return serial.load(fn_)
        else:
            minions = pki_dir_minions(opts)
        return minions
    except OSError as exc:
        log.error('Encountered OSError while evaluating  minions in PKI dir: {0}'.format(exc))
        return minions


