from configparser import ConfigParser 

"""
Server no longer active
"""

def config(filename="db.ini", section="postgresql"): 
    parser = ConfigParser()
    parser.read(filename)
    der_sdb = {}
    if parser.has_section(section):
        params = parser.items(section)
        for i in params:
            der_sdb[i[0]] = i[1]
    else: 
        raise Exception(f'section not found in db file.'.format(section, filename))
    return der_sdb
