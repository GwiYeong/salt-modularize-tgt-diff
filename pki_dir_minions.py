def _all_minions(self, expr=None):
    '''
    Return a list of all minions that have auth'd
    '''
    mlist = []
    for fn_ in salt.utils.data.sorted_ignorecase(os.listdir(os.path.join(self.opts['pki_dir'], self.acc))):
        if not fn_.startswith('.') and os.path.isfile(os.path.join(self.opts['pki_dir'], self.acc, fn_)):
            mlist.append(fn_)
    return {'minions': mlist, 'missing': []}

