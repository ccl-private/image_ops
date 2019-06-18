""" Example of wrapping a C function that takes C double arrays as input using
    the Numpy declarations from Cython """

# import both numpy and the Cython declarations for numpy
import numpy as np
cimport numpy as np

# if you want to use the Numpy-C-API from Cython
# (not strictly necessary for this example)
np.import_array()

cdef extern from "Python.h":
    const unsigned char* PyUnicode_AsUTF8(object unicode)

# cdefine the signature of our c function
cdef extern from "c_mod.h":
    void init()
    void c_str2numpy(unsigned char * str_array, double * out_array, int len)

# create the wrapper code, with numpy type annotations
def init_func():
    init()
def c_str2numpy_func(str str_array not None, np.ndarray[double, ndim=1, mode="c"] out_array not None):
    c_str2numpy(<unsigned char*> PyUnicode_AsUTF8(str_array),
                <double*> np.PyArray_DATA(out_array),
                out_array.shape[0])