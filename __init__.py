def __init__(self, opts):
    self.opts = opts
    self.serial = salt.payload.Serial(opts)
    self.cache = salt.cache.factory(opts)
    # TODO: this is actually an *auth* check
    if self.opts.get('transport', 'zeromq') in ('zeromq', 'tcp'):
        self.acc = 'minions'
    else:
        self.acc = 'accepted'

