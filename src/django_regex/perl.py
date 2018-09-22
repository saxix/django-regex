import re


def compile(perl_pattern):
    separator = perl_pattern[0]
    perl_pattern = perl_pattern.replace(r'\%s' % separator, chr(0))
    __, pattern, perl_options = perl_pattern.split(separator)
    pattern = pattern.replace(chr(0), separator)
    options = 0
    for opt in perl_options:
        if opt == 'i':
            options += re.IGNORECASE
        if opt == 'm':
            options += re.MULTILINE

    return re.compile(pattern, options)
