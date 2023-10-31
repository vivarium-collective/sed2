import json
from process_bigraph import Composite


def convert_path(path):
    if isinstance(path, list):
        path = tuple(path)
    elif not isinstance(path, tuple):
        path = (path,)
    return path


def key_for_value(d, looking):
    """
    Get the key associated with a value in a dictionary.
    """
    found = None
    for key, value in d.items():
        if looking == value:
            found = key
            break
    return found


class Node:

    def __init__(self, outer=None):
        self.inner = {}
        self.outer = outer
        self.value = None
        self.leaf = False

    def __getitem__(self, path):
        path = convert_path(path)
        return self.get_path(path)

    def __setitem__(self, path, value):
        path = convert_path(path)
        self.set_path(path, value)

    def set_path(self, path, value):
        '''
        Set a value at a path in the hierarchy.
        '''

        # this case only when called directly
        if len(path) == 0:
            if isinstance(value, Node):
                self.value = value.value
            else:
                self.value = value

        elif len(path) == 1:
            final = path[0]
            if isinstance(value, Node):
                raise Exception(
                    f"the store being inserted at {path} is already in a tree "
                    f"at {value.path_for()}: {value.get_value()}")
            else:
                down = self.get_path((final,))
                if down:
                    if not down.leaf:
                        Exception(f'trying to set the value {value} of a branch at {down.path_for()}')
                    down.value = value
                else:
                    Exception(
                        f'trying to set the value {value} at a path that does not exist {final} at {self.path_for()}')

        elif len(path) > 1:
            head = path[0]
            tail = path[1:]
            down = self.get_path((head,))
            if down:
                down.set_path(tail, value)
            else:
                Exception(f'trying to set the value {value} at a path that does not exist {path} at {self.path_for()}')

        else:
            raise Exception("this should never happen")

    def get_path(self, path):
        """
        Get the node at the given path relative to this node.
        """

        if path:
            step = path[0]
            if step == '..':
                child = self.outer
            else:
                child = self.inner.get(step)

            if child:
                return child.get_path(path[1:])
            else:
                raise Exception(
                    f'{path} is not a valid path from '
                    f'{self.path_for()}')
        return self

    def path_for(self):
        """
        Find the path to this node.
        """
        if self.outer:
            key = key_for_value(self.outer.inner, self)
            above = self.outer.path_for()
            return above + (key,)
        return tuple()

    def get_value(self, condition=None, f=None):
        """
        Pull the values out of the tree in a structure symmetrical to the tree.
        """
        if self.inner:
            return {
                key: f(child.get_value(condition, f))
                for key, child in self.inner.items()
                if condition(child)}
        return self.value

    def top(self):
        """
        Find the top of this tree.
        """

        if self.outer:
            return self.outer.top()
        return self


class Builder:
    def __init__(self):
        self.models = {}
        self.simulators = {}
        self.simulations = {}
        self.observables = {}
        self.data_generators = {}
        self.outputs = {}

        # TODO
        self.tree = Node()
        self.composite = {}

    def from_file(self, filepath):
        """initialize from file"""
        pass

    def compile(self):
        # TODO -- this should actually build the Composite state
        #
        # self.composite_state[simulation_id] = {
        #     '_type': 'step',
        #     'address': '',
        #     'config': {}
        # }
        pass

    def run(self):
        sim = Composite(self.composite)

    def add_model(
            self,
            model_id,
            path,
            language
    ):
        assert model_id not in self.models, f'model {model_id} already exists'
        self.models[model_id] = {
            'path': path,
            'language': language
        }

    def add_simulator(
            self,
            simulator_id,
            name, version,
            kisao_id
    ):
        assert simulator_id not in self.simulators, f'simulator {simulator_id} already exists'
        self.simulators[simulator_id] = {
            'name': name,
            'version': version,
            'kisao_id': kisao_id
        }

    def add_simulation(
            self,
            simulation_id,
            simulator_id,
            model_id,
            type,
            output_dir,
            start_time,
            end_time,
            number_of_points,
            kisao_id
    ):
        assert simulation_id not in self.simulations, f'simulation {simulation_id} already exists'
        self.simulations[simulation_id] = {
            'simulator_id': simulator_id,
            'model_id': model_id,
            'type': type,
            'output_dir': output_dir,
            'start_time': start_time,
            'end_time': end_time,
            'number_of_points': number_of_points,
            'kisao_id': f'KISAO:{kisao_id}'
        }

    def add_observable(
            self,
            observable_id,
            target_xpath
    ):
        self.observables[observable_id] = {
            'target_xpath': target_xpath
        }

    def add_data_generator(
            self,
            data_generator_id,
            operation,
            apply_to
    ):
        self.data_generators[data_generator_id] = {
            'operation': operation,
            'apply_to': apply_to
        }

    def add_output(
            self,
            output_id,
            type,
            data_generators
    ):
        self.outputs[output_id] = {
            'type': type,
            'data_generators': data_generators
        }

    def save_to_file(self, file_path):
        # Serialize the SED2 document to a JSON file
        with open(file_path, 'w') as f:
            f.write(json.dumps(self.composite, indent=2))


def test_builder_sed19():
    """Run multiple stochastic simulations, compute means and standard deviations."""

    # Initialize the Builder
    sed = Builder()

    # Load an SBML model
    sed.add_model(
        model_id='model1',
        path='demo_processes/BIOMD0000000061_url.xml',
        language='urn:sedml:language:sbml')

    # Set up the simulator
    sed.add_simulator(
        simulator_id='simulator1',
        name='Tellurium',
        version='2.1',
        kisao_id='0000029',  # Gillespie direct algorithm
    )

    # Define a stochastic simulation
    # sed.add_batch()  # TODO do we want to support navigating nested hierarchy?

    n_simulations = 100
    for i in range(n_simulations):
        sed.add_simulation(
            simulation_id=f'simulation_{i}',
            simulator_id='simulator1',
            model_id='model1',
            type='stochastic',
            output_dir=f'output_{i}',
            # number_of_runs=100,
            start_time=0,
            end_time=100,
            number_of_points=1000,
            kisao_id='0000029')

    # TODO -- this need to wait for all 100 sims to complete
    # Define an observable
    sed.add_observable(
        observable_id='observable1',
        target_xpath='path/to/observable1')

    # Set up a data generator for the mean
    sed.add_data_generator(
        data_generator_id='dataGen_mean_observable1',
        operation='mean',
        apply_to='observable1')

    # Set up a data generator for the standard deviation
    sed.add_data_generator(
        data_generator_id='dataGen_stddev_observable1',
        operation='stdDev',
        apply_to='observable1')

    # Define the output report
    sed.add_output(
        output_id='output1',
        type='report',
        data_generators=['dataGen_mean_observable1', 'dataGen_stddev_observable1'])

    # Save the SED2 document to a JSON file
    sed.save_to_file(
        file_path='my_simulation_experiment.sed')

    # Execute the simulation experiment
    results = sed.run()


if __name__ == '__main__':
    test_builder_sed19()
