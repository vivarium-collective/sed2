


class Node:
    def __init__(self, data, schema_keys):
        self._data = data
        self._schema_keys = schema_keys

    def __getattr__(self, item):
        # Special handling for schema keys
        schema_key = f'_{item}'
        if schema_key in self._schema_keys:
            return self._data.get(schema_key)
        raise AttributeError(f"{item} is not a valid attribute or schema key.")

    def __setattr__(self, key, value):
        if key in ['_data', '_schema_keys']:
            super().__setattr__(key, value)
        else:
            schema_key = f'_{key}'
            if schema_key in self._schema_keys:
                self._data[schema_key] = value
            else:
                raise AttributeError(f"{key} is not a valid attribute or schema key.")

    def __repr__(self):
        return f"Node({self._data})"


class Builder:
    def __init__(self, schema_keys=None, tree_dict=None):
        # Ensure that '_value' is always a part of the schema
        self.schema_keys = {'_value'}
        if schema_keys:
            self.schema_keys.update(f'_{key}' for key in schema_keys if not key.startswith('_'))
        self.bigraph = tree_dict if tree_dict is not None else {}

    def __getitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys,)

        current_dict = self.bigraph
        for key in keys:
            current_dict = current_dict.setdefault(key, {})

        return Node(current_dict, self.schema_keys)

    def __setitem__(self, keys, value):
        if not isinstance(keys, tuple):
            keys = (keys,)

        current_dict = self.bigraph
        for key in keys[:-1]:
            current_dict = current_dict.setdefault(key, {})

        # Assign the value to the '_value' key
        current_dict[keys[-1]] = {'_value': value}

    def __repr__(self):
        return f"Tree({self.bigraph})"



def test_tree():

    # Example usage:
    tree = Builder(schema_keys=['apply', 'parameters'])








if __name__ == '__main__':
    test_tree()
