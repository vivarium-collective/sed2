from sed2.builder import Builder


class SEDBuilder(Builder):
    def __init__(self, tree_dict=None):
        # Initialize the base Tree with the specific schema keys for SED-ML
        super().__init__(
            schema_keys=['models', 'simulators', 'simulations', 'data_generators', 'observables'],
            tree_dict=tree_dict)

    def add_model(self, model_id, path, language):
        # Add a model to the 'models' dictionary
        self['models'][model_id] = {
            '_path': path,
            '_language': language
        }

    def add_simulator(self, simulator_id, name, version, kisao_id):
        # Add a simulator to the 'simulators' dictionary
        self['simulators'][simulator_id] = {
            '_name': name,
            '_version': version,
            '_kisao_id': kisao_id
        }

    def add_simulation(
            self,
            simulation_id,
            simulator_id,
            model_id,
            start_time,
            end_time,
            number_of_points,
            kisao_id
    ):
        # Ensure the simulation ID is unique
        assert simulation_id not in self['simulations'], f"Simulation '{simulation_id}' already exists."
        # Add a simulation to the 'simulations' dictionary
        self['simulations'][simulation_id] = {
            '_simulator_id': simulator_id,
            '_model_id': model_id,
            '_start_time': start_time,
            '_end_time': end_time,
            '_number_of_points': number_of_points,
            '_kisao_id': f'KISAO:{kisao_id}'
        }

def test_builder():
    # Example usage:
    sed = SEDBuilder()

    # Load an SBML model
    sed.add_model(
        model_id='model1',
        path='demo_processes/BIOMD0000000061_url.xml',
        language='urn:sedml:language:sbml',
    )

    # Set up the simulator
    sed.add_simulator(
        simulator_id='simulator1',
        name='Tellurium',
        version='2.1',
        kisao_id='0000029',  # Gillespie direct algorithm
    )

    # Print the SEDBuilder structure
    print(sed)





if __name__ == '__main__':
    test_builder()
