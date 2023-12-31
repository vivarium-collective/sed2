from process_bigraph import process_registry

from demo_processes.copasi_processes import CopasiProcess
from demo_processes.tellurium_process import TelluriumProcess
from demo_processes.cobra_process import CobraProcess
from demo_processes.demo_processes import Plot2D, DataOperation


process_registry.register('copasi', CopasiProcess)
process_registry.register('tellurium', TelluriumProcess)
process_registry.register('cobra', CobraProcess)
process_registry.register('line', Plot2D)
process_registry.register('data_operation', DataOperation)