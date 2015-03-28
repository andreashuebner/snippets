import logging
import argparse
import sys
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    # Subparser for the put command
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Get a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))

def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    try:
        with connection,connection.cursor() as cursor:
            command = "insert into snippets values (%s, %s)"
            cursor.execute(command, (name, snippet))
            
    except psycopg2.IntegrityError as e:
        with connection,connection.cursor() as cursor:
            command = "update snippets set message=%s where keyword=%s"
            cursor.execute(command, (snippet, name))
        
    
    
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, throw runtime error

    Returns the snippet.
    """
    
    logging.info("Retrieving snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()
    if row == None:
        raise RuntimeError("Snippet {!r} does not exist".format(name))
    message = row[0]
    logging.info("Have retrieved snippet {!r}".format(message))
    return message

if __name__ == "__main__":
    
    main()