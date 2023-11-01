# from process_bigraph.type_system import types  #ProcessTypes
import pprint
from sed2.builder import Builder

pretty = pprint.PrettyPrinter(indent=2)


def pp(x):
    """Print ``x`` in a pretty format."""
    pretty.pprint(x)


def pf(x):
    """Format ``x`` for display."""
    return pretty.pformat(x)


# types = ProcessTypes()   # TODO -- how will Composite know these types?
# types.type_registry.register_multiple(sed_types)
