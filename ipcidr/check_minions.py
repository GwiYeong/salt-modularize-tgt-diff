def _check_ipcidr_minions(self, expr, greedy):
    '''
    Return the minions found by looking via ipcidr
    '''
    cache_enabled = self.opts.get('minion_data_cache', False)

    if greedy:
        minions = self._pki_minions()
    elif cache_enabled:
        minions = self.cache.list('minions')
    else:
        return {'minions': [],
                'missing': []}

    if cache_enabled:
        if greedy:
            cminions = self.cache.list('minions')
        else:
            cminions = minions
        if cminions is None:
            return {'minions': minions,
                    'missing': []}

        tgt = expr
        try:
            # Target is an address?
            tgt = ipaddress.ip_address(tgt)
        except:  # pylint: disable=bare-except
            try:
                # Target is a network?
                tgt = ipaddress.ip_network(tgt)
            except:  # pylint: disable=bare-except
                log.error('Invalid IP/CIDR target: {0}'.format(tgt))
                return {'minions': [],
                        'missing': []}
        proto = 'ipv{0}'.format(tgt.version)

        minions = set(minions)
        for id_ in cminions:
            mdata = self.cache.fetch('minions/{0}'.format(id_), 'data')
            if mdata is None:
                if not greedy:
                    minions.remove(id_)
                continue
            grains = mdata.get('grains')
            if grains is None or proto not in grains:
                match = False
            elif isinstance(tgt, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
                match = str(tgt) in grains[proto]
            else:
                match = salt.utils.network.in_subnet(tgt, grains[proto])

            if not match and id_ in minions:
                minions.remove(id_)

    return {'minions': list(minions),
            'missing': []}

