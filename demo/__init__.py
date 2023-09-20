from process_bigraph import process_registry

from demo.copasi_processes import CopasiProcess
from demo.tellurium_process import TelluriumProcess
from demo.demo_processes import Plot2D


process_registry.register('copasi', CopasiProcess)
process_registry.register('tellurium', TelluriumProcess)
process_registry.register('plot2d', Plot2D)
