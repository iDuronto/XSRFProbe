#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:#
#    XSRFProbe     #
#-:-:-:-:-:-:-:-:-:#

# Author: @_tID
# This module requires XSRFProbe
# https://github.com/0xInfection/XSRFProbe

import time
import urllib.parse
from math import log
from core.colors import *
from .Token import Token
from core.verbout import verbout

def Entropy(req, url, m_action, m_name=''):
    """
    This function has the work of comparing and
      calculating Shannon Entropy and related
           POST Based requests' security.

    """

    # The minimum length of a csrf token should be 5 bytes.
    min_length = 5

    # I have never seen a CSRF token longer than 256 bytes,
    # so the main concept here is doubling that and checking
    # to make sure we don't check parameters which are
    # files in multipart uploads or stuff like that.
    #
    # Multipart uploads usually have a trailing sequence of
    # characters which could be misunderstood as a CSRF token.
    # This is a very important step with respect to
    # decreasing [[ False Positives ]].
    max_length = 256*2

    # Shannon Entropy calculated for a particular CSRF token
    # should be at least 2.4. If the token entropy is less
    # than that, the application request can be easily
    # forged making the application vulnerable even in
    # presence of a CSRF token.
    min_entropy = 2.4

    # Check for common CSRF token names
    _q, para = Token(req)
    if (para and _q) == '':
        return '', ''
    # Coverting the token to a raw string, cause some special
    # chars might fu*k with the Shannon Entropy operation.
    value = r'%s' % para

    # Check length
    if len(value) <= min_length:
        print(color.RED+' [-] CSRF Token Length less than 5 bytes. '+color.ORANGE+'Token value can be guessed/bruteforced...')
        print(color.ORANGE+' [-] Endpoint likely '+color.BR+' VULNERABLE '+color.END+color.ORANGE+' to CSRF Attacks...')
        print(color.ORANGE+' [!] Vulnerability Type: '+color.BG+' Very Short/No Anti-CSRF Tokens '+color.END)
    if len(value) > max_length:
        print(color.GREEN+' [+] CSRF Token Length greater than 256 bytes. '+color.ORANGE+'Token value cannot be guessed/bruteforced...')
        print(color.ORANGE+' [+] Endpoint likely '+color.BG+' NOT VULNERABLE '+color.END+color.ORANGE+' to CSRF Attacks...')
        print(color.ORANGE+' [!] CSRF Mitigation Method: '+color.BG+' Long Anti-CSRF Tokens '+color.END)

    # Calculate entropy
    verbout(O, 'Proceeding to calculate '+color.GREY+'Shannon Entropy'+color.END+' of Token audited...')
    entropy = calcEntropy(value)
    verbout(GR, 'Calculating Entropy...')
    verbout(color.BLUE, ' [+] Entropy Calculated: '+color.CYAN+str(entropy))
    if entropy >= min_entropy:
        verbout(color.ORANGE,' [+] Anti-CSRF Token Entropy Calculated is '+color.BY+' GREATER than 2.4 '+color.END+'... ')
        print(color.ORANGE+' [+] Endpoint '+color.BG+' NOT VULNERABLE '+color.END+color.ORANGE+' to CSRF Attacks...')
        print(color.ORANGE+' [!] CSRF Mitigation Method: '+color.BG+' High Entropy Anti-CSRF Tokens '+color.END)
    else:
        verbout(color.RED,' [-] Anti-CSRF Token Entropy Calculated is '+color.BY+' LESS than 2.4 '+color.END+'... ')
        print(color.ORANGE+' [-] Endpoint likely '+color.BR+' VULNERABLE '+color.END+color.ORANGE+' to CSRF Attacks inspite of CSRF Tokens...')
        print(color.ORANGE+' [!] Vulnerability Type: '+color.BR+' Low Entropy Anti-CSRF Tokens '+color.END)
        if m_name:
            print(color.RED+'\n +---------+')
            print(color.RED+' |   PoC   |')
            print(color.RED+' +---------+\n')
            print(color.BLUE+' [+] URL : ' +color.CYAN+url)
            print(color.CYAN+' [+] Name : ' +color.ORANGE+m_name)
            print(color.GREEN+' [+] Action : ' +color.ORANGE+m_action)
        else:  # if value m_name not there :(
            print(color.RED+'\n +---------+')
            print(color.RED+' |   PoC   |')
            print(color.RED+' +---------+\n')
            print(color.BLUE+' [+] URL : ' +color.CYAN+url)
            print(color.GREEN+' [+] Action : ' +color.ORANGE+m_action)
        # Print out the params
        print(color.ORANGE+' [+] Query : '+color.GREY+urllib.parse.urlencode(result))
        print('')
    return _q, para  # Return the query paramter and anti-csrf token

def calcEntropy(data):
    """
    This function is used to calculate
              Shannon Entropy.
    """
    if not data:
        return 0

    entropy = 0 # init

    for x in range(256):
        p_x = float(data.count(chr(x)))/len(data)
        if p_x > 0:
            entropy += - p_x * log(p_x, 2)

    return entropy
