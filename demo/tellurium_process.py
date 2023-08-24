"""
Tellurium Process
"""
from process_bigraph import Process, Composite, process_registry
import tellurium


class TelluriumProcess(Process):
    config_schema = {'model_file': 'string'}

    def __init__(self, config=None):
        super().__init__(config)

        # initialize a tellurium(roadrunner) simulation object. Load the model in using either sbml(default) or antimony
        self.simulator = tellurium.loadSBMLModel(self.config['model_file'])

        # extract the variables
        self.floating_species_list = self.simulator.getFloatingSpeciesIds()
        self.boundary_species_list = self.simulator.getBoundarySpeciesIds()
        self.reaction_list = self.simulator.getReactionIds()

    @classmethod
    def load(cls, sbml_model):
        return cls({'model_file': sbml_model})

    def schema(self):
        return {
            'floating_species': {
                species_id: 'float' for species_id in self.floating_species_list},
            'boundary_species': {
                species_id: 'float' for species_id in self.boundary_species_list},
            'reactions': {
                reaction_id: 'float' for reaction_id in self.reaction_list},
        }

    def update(self, state, interval):
        # set the states in tellurium according to what is passing in states
        for species_id, value in state['species'].items():
            self.tellurium_object.set_species(species_id, value)

        # run the simulation
        self.tellurium_object.simulate(0, interval, 1)

        # extract the results. TODO -- get the final values of the self.config['exposed_species'] and put them in the update
        update = {'species': {}}
        results = self.tellurium_object.get_data()

        return update


process_registry.register('tellurium', TelluriumProcess)


def test_process():

    sbml_schema = {
        'floating_species_store': 'tree[any]',
        'boundary_species_store': 'tree[any]',
        'reactions_store': 'tree[any]',
        'tellurium': {
            '_type': 'process',
            '_ports': {
                'floating_species': 'tree[any]',
                'boundary_species': 'tree[any]',
                'reactions': 'tree[any]',
            }
        },
    }

    # this is the instance for the composite process to run
    initial_sim_state = {
        # 'floating_species_store': {},
        # 'boundary_species_store': {},
        # 'reactions_store': {},
        'tellurium': {
            'address': 'local:tellurium',  # using a local toy process
            'config': {
                'model_file': '"demo/Caravagna2010.xml"'
            },
            'interval': '1.0',
            'wires': {
                'floating_species': 'floating_species_store',
                'boundary_species': 'boundary_species_store',
                'reactions': 'reactions_store'
            }
        },
    }

    # make the composite
    workflow = Composite({
        'composition': sbml_schema,
        'schema': {
            'results': 'tree[any]'},
        'bridge': {
            'results': ['fluxes']},
        'state': initial_sim_state
    })

    # run
    update = workflow.update({}, 1)
    print(f'UPDATE: {update}')


if __name__ == '__main__':
    test_process()
