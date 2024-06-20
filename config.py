from configparser import ConfigParser

def config(filename='database.ini',section='postgresql'):
    # Create parser
    parser = ConfigParser()

    # Read config_file
    parser.read(filename)

    # Initialize db
    db = {}

    # Check to see if the section (psql) parser exists
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    # Return error if a param is called and not listed in .ini file
    else:
        raise Exception(
            'Section{0} is not found in the {1} file.'.format(section,filename)
        )
    return db