class DataBase:

    data_dict = {}             # Holds the actual data entered by the user
    multi_activated = False    # Handles the Transaction Commands
    rollback_trans = []        # Save the Commands to RollBack in case of discard
    reverse_dict = {}          # Reverse Dict to get data by values in less then O(N)

    def is_input_valid(self, key=None, value=None):
        if key and not isinstance(key, str):
            print("Key Value is invalid: String Expected")
            return False

        if value and not isinstance(value, int):
            print("Value is invalid: Integer Expected")
            return False

        return True

    def get(self, key):
        if not self.is_input_valid(key=key):
            return

        value = self.data_dict.get(key)
        if not value:
            print('<nil>')
            return

        print(value)
        return value

    def set(self, key, value):
        if not self.is_input_valid(key=key, value=value):
            return

        # Automatically replace the value if already exists
        self.data_dict[key] = value

        previous_values = self.reverse_dict.get(value, [])
        previous_values.append(key)
        self.reverse_dict[value] = previous_values

        if self.multi_activated:
            # Add roll Back Command
            command = 'DEL {}'.format(key)
            self.rollback_trans.append(command)

    def increment(self, key):
        if not self.is_input_valid(key=key):
            return

        # previous value
        p_value = self.data_dict.get(key, 0)
        new_value = p_value + 1
        self.data_dict[key] = new_value

        reversed_keys = self.reverse_dict.get(p_value)
        if reversed_keys:
            self.reverse_dict[p_value].remove(key)
        self.reverse_dict[new_value] = self.reverse_dict.get(new_value, []) + [key]

        if self.multi_activated:
            # Add roll Back Command
            command = 'DECR {}'.format(key)
            self.rollback_trans.append(command)

        return new_value

    def decrement(self, key):
        if not self.is_input_valid(key=key):
            return

        # previous value
        p_value = self.data_dict.get(key)
        if p_value:
            new_value = p_value - 1
            self.data_dict[key] = new_value

            revesed_keys = self.reverse_dict.get(p_value)
            if revesed_keys:
                self.reverse_dict[p_value].remove(key)
            self.reverse_dict[new_value] = self.reverse_dict.get(new_value, []) + [key]

    def delete(self, key):
        if not self.is_input_valid(key=key):
            return

        if self.multi_activated:
            # Add roll Back Command
            value = self.data_dict.get(key)
            command = 'SET {} {}'.format(key, value)
            self.rollback_trans.append(command)

        value = self.data_dict.get(key)
        if value:
            del self.data_dict[key]
            print("Value for Key: {} is deleted".format(key))

            reversed_keys = self.reverse_dict.get(value)
            reversed_keys.remove(key)
            self.reverse_dict[value] = reversed_keys

    def delete_value(self, value):
        if not self.is_input_valid(value=value):
            return

        # O(N) search method
        # new_data = {k: v for k, v in self.data_dict.items() if v != value}
        # self.data_dict = new_data

        keys_to_delete = self.reverse_dict.get(value, [])
        for key in keys_to_delete:

            if self.multi_activated:
                command = 'SET {} {}'.format(key, value)
                self.rollback_trans.append(command)

            self.data_dict.pop(key)

        self.reverse_dict.pop(value, 'Key does not exist')

    def multi(self):
        self.multi_activated = True

    def discard(self):
        if not self.rollback_trans:
            print('NOT IN TRANSACTION')
        else:
            self.multi_activated = False

            for command in self.rollback_trans:
                self.execute_command(command)

            print(len(self.rollback_trans))
            self.rollback_trans = []
            self.multi_activated = True

    def exec(self):
        if not self.rollback_trans:
            print('NOT IN TRANSACTION')
        else:
            print(len(self.rollback_trans))
            self.rollback_trans = []

    def execute_command(self, command):
        if command == 'MULTI':
            self.multi()
            return

        if command == 'EXEC':
            self.exec()
            return

        if command == 'DISCARD':
            self.discard()
            return

        if 'GET' in command:
            command, key = command.split()
            self.get(key)

        if 'SET' in command:
            command, key, value = command.split()
            self.set(key, int(value))

        if 'INCR' in command:
            command, key = command.split()
            self.increment(key)

        if 'DECR' in command:
            command, key = command.split()
            self.decrement(key)

        if 'DELVALUE' in command:
            command, value = command.split()
            self.delete_value(int(value))

        if 'DEL' in command:
            command, key = command.split()
            self.delete(key)
