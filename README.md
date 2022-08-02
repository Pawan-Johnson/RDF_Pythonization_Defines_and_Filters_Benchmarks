# RDF_Pythonization_Defines_and_Filters_Benchmarks
Contains the code used in benchmarking the Pythonized Define and Filters of ROOT's RDataFrame

The files must be run in Python with a ROOT version that supports the Pythonized version of the Defines and Filter.
Preferable use the following branch:
https://github.com/Pawan-Johnson/root/tree/RDFPythonization-Defines

## To check speed difference between Pythonizations to CPP
Run the following files 
1. Cpp_Operations.py : Runs the Defines and Filters using functions declared using gInterpreter.
2. Py_Operations.py : Runs the Defines and Filters using python functions.
3. NbD_Operations.py: Runs the Defines and Filters using the Numba Declared Python Functions.

## To see the time taken againt number of operations
Run NOperations.py . This takes a command line argument which defines the number of operations.
