#include <Python.h>
#include <iostream>

int main()
{
    // Initialize the Python Interpreter
    Py_Initialize();

    // Add the current directory to the Python path
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append(\".\")");

    // Import the proxy module
    PyObject* pName = PyUnicode_DecodeFSDefault("proxy");
    PyObject* pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != nullptr) {
        // Get the run function from the module
        PyObject* pFunc = PyObject_GetAttrString(pModule, "run");

        // Check if the function is callable
        if (PyCallable_Check(pFunc)) {
            // Call the run function
            PyObject* pValue = PyObject_CallObject(pFunc, nullptr);
            if (pValue != nullptr) {
                Py_DECREF(pValue);
            }
            else {
                PyErr_Print();
                std::cerr << "Call to run() failed" << std::endl;
            }
        }
        else {
            if (PyErr_Occurred()) PyErr_Print();
            std::cerr << "Cannot find function 'run'" << std::endl;
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else {
        PyErr_Print();
        std::cerr << "Failed to load 'proxy' module" << std::endl;
    }

    // Finalize the Python Interpreter
    Py_Finalize();

    return 0;
}