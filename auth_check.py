def auth_check(self,
               auth_list,
               funs,
               args,
               tgt,
               tgt_type='glob',
               groups=None,
               publish_validate=False,
               minions=None,
               whitelist=None):
    '''
    Returns a bool which defines if the requested function is authorized.
    Used to evaluate the standard structure under external master
    authentication interfaces, like eauth, peer, peer_run, etc.
    '''
    if self.opts.get('auth.enable_expanded_auth_matching', False):
        return self.auth_check_expanded(auth_list, funs, args, tgt, tgt_type, groups, publish_validate)
    if publish_validate:
        v_tgt_type = tgt_type
        if tgt_type.lower() in ('pillar', 'pillar_pcre'):
            v_tgt_type = 'pillar_exact'
        elif tgt_type.lower() == 'compound':
            v_tgt_type = 'compound_pillar_exact'
        _res = self.check_minions(tgt, v_tgt_type)
        v_minions = set(_res['minions'])

        _res = self.check_minions(tgt, tgt_type)
        minions = set(_res['minions'])

        mismatch = bool(minions.difference(v_minions))
        # If the non-exact match gets more minions than the exact match
        # then pillar globbing or PCRE is being used, and we have a
        # problem
        if mismatch:
            return False
    # compound commands will come in a list so treat everything as a list
    if not isinstance(funs, list):
        funs = [funs]
        args = [args]
    try:
        for num, fun in enumerate(funs):
            if whitelist and fun in whitelist:
                return True
            for ind in auth_list:
                if isinstance(ind, six.string_types):
                    # Allowed for all minions
                    if self.match_check(ind, fun):
                        return True
                elif isinstance(ind, dict):
                    if len(ind) != 1:
                        # Invalid argument
                        continue
                    valid = next(six.iterkeys(ind))
                    # Check if minions are allowed
                    if self.validate_tgt(
                        valid,
                        tgt,
                        tgt_type,
                        minions=minions):
                        # Minions are allowed, verify function in allowed list
                        fun_args = args[num]
                        fun_kwargs = fun_args[-1] if fun_args else None
                        if isinstance(fun_kwargs, dict) and '__kwarg__' in fun_kwargs:
                            fun_args = list(fun_args)  # copy on modify
                            del fun_args[-1]
                        else:
                            fun_kwargs = None
                        if self.__fun_check(ind[valid], fun, fun_args, fun_kwargs):
                            return True
    except TypeError:
        return False
    return False

