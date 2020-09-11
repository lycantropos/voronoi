#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <sstream>
#include <stdexcept>

#include "voronoi.hpp"

namespace py = pybind11;

#define MODULE_NAME _voronoi
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(Python binding of pyvoronoi library.)pbdoc";

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
