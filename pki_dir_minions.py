def pki_dir_minions(opts):
    acc = pki_dir_acc_path(opts)
    minions = []
    for fn_ in salt.utils.data.sorted_ignorecase(os.listdir(os.path.join(opts['pki_dir'], acc))):
        if not fn_.startswith('.') and os.path.isfile(os.path.join(opts['pki_dir'], acc, fn_)):
            minions.append(fn_)
    return minions


