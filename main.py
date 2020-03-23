from data_base import DataBase


def main():
    error_msg = "Please enter a valid command from the following " \
                "['GET', 'SET', 'INCR', 'DEL', 'DELVALUE', 'MULTI', 'DISCARD', 'EXEC', 'DECR']"
    db = DataBase()

    while True:
        var = input()
        try:
            command = var.split()[0]
            if command in ['GET', 'SET', 'INCR', 'DEL', 'DELVALUE', 'MULTI', 'DISCARD', 'EXEC', 'DECR']:
                db.execute_command(var)

        except (IndexError, KeyError, ValueError):
            print(error_msg)
            continue


# Call main function
if __name__ == "__main__":
    main()
