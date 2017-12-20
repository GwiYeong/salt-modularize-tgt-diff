def pki_dir_acc_path(opts):
    # TODO: this is actually an *auth* check
    if opts.get('transport', 'zeromq') in ('zeromq', 'tcp'):
        return 'minions'
    else:
        return 'accepted'


