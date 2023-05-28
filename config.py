host = "dpg-chev3b0rddl9bukdq8m0-a.oregon-postgres.render.com"
port = '5432'
dbname = "db_for_project"
user = "user"
password = "qByfP0Y0fVZrcnAaMO7soqJEhynv4wdu"
# postgres://user:qByfP0Y0fVZrcnAaMO7soqJEhynv4wdu@dpg-chev3b0rddl9bukdq8m0-a.oregon-postgres.render.com/db_for_project


def generate_key(data):
    """
    Method for transforming value to string with several changes
    :param data: number as string - part of IP-address
    :return: transforming part of index for database
    """
    return str(int(data) * 2)
