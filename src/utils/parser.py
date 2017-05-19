import re


def database_parser(dburl):
    """
    Parses the database.

    :param dburl: The url of the Postgres database.
    :return: Tuple (user_name, user_password, db_host, db_port, db_name)
    """
    m = re.search('postgres://([\w]*):([\w]*)@([^\s]*):([0-9]*)/([\w]*)', dburl)
    user_name = m.group(1)
    user_password = m.group(2)
    db_hostname = m.group(3)
    db_port_number = m.group(4)
    db_name = m.group(5)
    return user_name, user_password, db_hostname, db_port_number, db_name
