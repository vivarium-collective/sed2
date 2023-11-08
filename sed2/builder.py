import json
import os
import uuid
import pprint
from process_bigraph import Composite


pretty = pprint.PrettyPrinter(indent=2)


def pf(x):
    """Format ``x`` for display."""
    return pretty.pformat(x)


class Node:
    """
    Provides attribute-style access to the data within a tree
    """
    def __init__(self, data, schema_keys, path, builder):
        self._data = data
        self._schema_keys = schema_keys
        self._path = path  # Store the current path
        self._builder = builder  # Reference to the builder instance

    def __getattr__(self, item):
        schema_key = f'_{item}'
        if schema_key in self._schema_keys:
            return self._data.get(schema_key)
        raise AttributeError(f"{item} is not a valid attribute or schema key.")

    def __setattr__(self, key, value):
        if key in ['_data', '_schema_keys', '_path', '_builder']:
            super().__setattr__(key, value)
        else:
            schema_key = f'_{key}'
            if schema_key in self._schema_keys:
                self._data[schema_key] = value
            else:
                raise AttributeError(f"{key} is not a valid attribute or schema key.")

    def __repr__(self):
        return f"Node({self._data})"

    def add_process(self, process_id, process_type=None, address=None, config=None):
        # Add the process with the given ID and attributes
        self._data[process_id] = {
            '_type': process_type or 'step',
            'address': address,
            'config': config,
            'wires': {},
        }

        # Update the builder's tree_dict
        self._builder.update_tree(self._path, self._data)


class Builder:
    schema_keys = {'_value'}

    def __init__(self, schema_keys=None, bigraph_dict=None):
        if schema_keys:
            self.schema_keys.update(f'_{key}' for key in schema_keys if not key.startswith('_'))
        self.bigraph = bigraph_dict or {}

    def __getitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys,)

        current_dict = self.bigraph
        for key in keys:
            current_dict = current_dict.setdefault(key, {})

        return Node(current_dict, self.schema_keys, keys, self)

    def __setitem__(self, keys, value):
        if not isinstance(keys, tuple):
            keys = (keys,)

        current_dict = self.bigraph
        for key in keys[:-1]:
            current_dict = current_dict.setdefault(key, {})

        # Assign the value to the '_value' key
        current_dict[keys[-1]] = {'_value': value}

    def update_tree(self, path, data):
        # Navigate to the correct location in the tree and update the data
        current_dict = self.bigraph
        for key in path[:-1]:
            current_dict = current_dict.setdefault(key, {})
        current_dict[path[-1]] = data

    def __repr__(self):
        return f"Bigraph({self.bigraph})"


class SEDBuilder(Builder):
    def __init__(self, bigraph_dict=None):
        # Initialize with the specific schema keys for SED
        super().__init__(
            schema_keys=['annotations', ],
            bigraph_dict=bigraph_dict)

        self.models = {}
        self.simulators = {}

    def add_task(self, task_id=None):
        task_id = task_id or str(uuid.uuid1())

        # TODO -- make do this part entirely with Builder API. add_process
        # self.add_process()

    def add_resource(self):
        pass

    def add_model(
            self,
            model_id,
            source,
            language=None,
            changes=None,
    ):
        # Ensure the model ID is unique
        assert model_id not in self.models, f"Model '{model_id}' already exists."
        # Add a model to the 'models' dictionary
        self.models[model_id] = {
            'source': source,
            'language': f'urn:sedml:language:{language}'
        }

    def add_dataset(self):
        pass

    def add_simulator(self, simulator_id, name, version, kisao_id):
        # Ensure the simulator ID is unique
        assert simulator_id not in self.simulators, f"Simulator '{simulator_id}' already exists."
        # Add a simulator to the 'simulators' dictionary
        self.simulators[simulator_id] = {
            'name': name,
            'version': version,
            'kisao_id': f'KISAO:{kisao_id}'
        }

    def add_simulation(
            self,
            simulation_id,
            simulator_id,
            model_id,
            start_time=None,
            end_time=None,
            number_of_points=None,
            observables=None,  # TODO to capture all model variables, omit this or have a method to specify all.
    ):
        # get the model
        model_source = self.models[model_id]['source']

        # TODO -- kisao ID should set the config shape and ports
        kisao_id = self.simulators[simulator_id]['kisao_id']

        # simulator name
        simulator_name = self.simulators[simulator_id]['name']

        # build up the bigraph
        self.bigraph[self.current_step_id][simulation_id] = {
            '_type': 'step',
            'address': f'local:{simulator_name}',  # TODO -- make protocol configurable
            'config': {  # TODO -- this has to be the standardized config of a given simulator instance
                'model_file': model_source,
                'kisao_id': kisao_id,
                # 'start_time': start_time,
                # 'end_time': end_time,
                # 'number_of_points': number_of_points,
                'observables': observables,
            },
            'wires': {},  # TODO -- add wires
            # '_depends_on': self.previous_step_id
        }

    def add_data_generator(
            self,
            data_id,
            simulation_id=None,  # TODO
            observables=None,
            operations=None,
            generator_id='data_operation',
    ):
        # build up the bigraph
        self.bigraph[self.current_step_id][data_id] = {
            '_type': 'step',
            'address': f'local:{generator_id}',
            'config': {
                'observables': observables,
                'operations': operations,
            },
            'wires': {},  # TODO
            # '_depends_on': self.previous_step_id  # TODO -- can this be done entirely based on wires?
        }

    def add_visualization(
            self,
            plot_id,
            plot_type=None,
            title=None,
            x_label=None,
            y_label=None,
            legend=None,
    ):
        # build up the bigraph
        self.bigraph[self.current_step_id][plot_id] = {
            '_type': 'step',
            'address': f'local:{plot_type}',
            'config': {
                # 'plot_type': plot_type,
                'title': title,
                'x_label': x_label,
                'y_label': y_label,
                'legend': legend,
            },
            'wires': {},  # TODO
            # '_depends_on': self.previous_step_id
        }

    def print_sed_doc(self):
        print(pf(self.bigraph))

    def save_sed_doc(self, filename=None, out_dir='out'):
        composite_dict = self.bigraph
        file_path = os.path.join(out_dir, filename)
        with open(file_path, 'w') as file:
            json.dump(composite_dict, file, indent=4)

    def save_archive(self):
        """save all the models and metadata in an archive"""
        pass



def test_tree():
    # Example usage:
    tree = Builder(schema_keys=['apply', 'parameters'])

    tree = Builder(schema_keys=['apply', 'parameters'])

    # add a branch with a value
    tree['a', 'b'] = 2.0
    tree['a', 'b2', 'c'] = 12.0

    # access and print the 'apply' attribute
    print(tree['a', 'b'].apply)  # Output: None
    tree['a', 'b'].apply = 'sum'
    print(tree['a', 'b'].apply)  # Output: 'sum'
    print(tree['a', 'b'].value)  # Output: 2.0

    # add a process

    tree['a', 'b2'].add_process(process_id='p1')
    tree


    # test with preloaded dict
    tree2 = Builder(bigraph_dict={'path': {'to': {'leaf': {'_value': 1.0}}}}, schema_keys=['apply', 'parameters'])




def test_sedbuilder():
    sed = SEDBuilder()
    sed


if __name__ == '__main__':
    test_tree()
