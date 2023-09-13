"""
Tellurium Process
"""
from process_bigraph import Process, Composite, process_registry
import tellurium as te


class TelluriumProcess(Process):
    config_schema = {
        'sbml_model_path': 'string',
        'antimony_string': 'string',
    }

    def __init__(self, config=None):
        super().__init__(config)

        # initialize a tellurium(roadrunner) simulation object. Load the model in using either sbml(default) or antimony
        if self.config.get('antimony_string') and not self.config.get('sbml_model_path'):
            self.simulator = te.loada(self.config['antimony_string'])
        elif self.config.get('sbml_model_path') and not self.config.get('antimony_string'):
            self.simulator = te.loadSBMLModel(self.config['sbml_model_path'])
        else:
            raise Exception('the config requires either an "antimony_string" or an "sbml_model_path"')

        # TODO -- make this configurable.
        self.input_ports = [
            'floating_species',
            'boundary_species',
            'model_parameters'
            # 'time',
            # 'compartments',
            # 'parameters',
            # 'stoichiometries',
        ]

        self.output_ports = [
            'floating_species',
            # 'time',
        ]

        # Get the species (floating and boundary
        self.floating_species_list = self.simulator.getFloatingSpeciesIds()
        self.boundary_species_list = self.simulator.getBoundarySpeciesIds()
        self.floating_species_initial = self.simulator.getFloatingSpeciesConcentrations()
        self.boundary_species_initial = self.simulator.getBoundarySpeciesConcentrations()

        # Get the list of parameters and their values
        self.model_parameters_list = self.simulator.getGlobalParameterIds()
        self.model_parameter_values = self.simulator.getGlobalParameterValues()

        # Get a list of reactions
        self.reaction_list = self.simulator.getReactionIds()

    def initial_state(self, config=None):
        floating_species_dict = dict(zip(self.floating_species_list, self.floating_species_initial))
        boundary_species_dict = dict(zip(self.boundary_species_list, self.boundary_species_initial))
        model_parameters_dict = dict(zip(self.model_parameters_list, self.model_parameter_values))
        return {
            'time': 0.0,
            'floating_species': floating_species_dict,
            'boundary_species': boundary_species_dict,
            'model_parameters': model_parameters_dict
        }

    @classmethod
    def load(cls, sbml_model):
        return cls({'model_file': sbml_model})

    def schema(self):
        return {
            'time': 'float',
            'floating_species': {
                species_id: 'float' for species_id in self.floating_species_list},
            'boundary_species': {
                species_id: 'float' for species_id in self.boundary_species_list},
            'model_parameters': {
                param_id: 'float' for param_id in self.model_parameters_list},
            'reactions': {
                reaction_id: 'float' for reaction_id in self.reaction_list},
        }

    def update(self, state, interval):

        # set tellurium values according to what is passed in states
        for port_id, values in state.items():
            if port_id in self.input_ports:  # only update from input ports
                for cat_id, value in values.items():
                    self.simulator.setValue(cat_id, value)

        # run the simulation
        new_time = self.simulator.oneStep(state['time'], interval)

        # extract the results and convert to update
        update = {'time': new_time}
        for port_id, values in state.items():
            if port_id in self.output_ports:
                update[port_id] = {}
                for cat_id in values.keys():
                    update[port_id][cat_id] = self.simulator.getValue(cat_id)
        return update


process_registry.register('tellurium', TelluriumProcess)


def test_process():

    # this is the instance for the composite process to run
    instance = {
        'tellurium': {
            '_type': 'process',
            'address': 'local:tellurium',  # using a local toy process
            'config': {
                'sbml_model_path': '"demo/BIOMD0000000061_url.xml"',
            },
            # 'interval': '1.0',
            'wires': {
                'time': 'time_store',
                'floating_species': 'floating_species_store',
                'boundary_species': 'boundary_species_store',
                'model_parameters': 'model_parameters_store',
                'reactions': 'reactions_store',
            }
        },
        'emitter': {
            '_type': 'step',
            'address': 'local:ram-emitter',
            'config': {
                'ports': {
                    'inputs': {
                        'floating_species': 'tree[float]'
                    }
                }
            },
            'wires': {
                'inputs': {
                    'floating_species': ['floating_species_store'],
                }
            }
        }
    }

    # make the composite
    workflow = Composite({
        # 'schema': {
        #     'results': 'tree[any]'},
        # 'bridge': {
        #     'results': ['fluxes']},
        'state': instance
    })

    # initial_state = workflow.initial_state()

    # run
    update = workflow.update(
        {}, 10)
    print(f'UPDATE: {update}')

    # gather results
    results = workflow.gather_results()
    print(f'RESULTS: {results}')



if __name__ == '__main__':
    test_process()
