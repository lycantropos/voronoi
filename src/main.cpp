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
#define POINT_NAME "Point"
#define SEGMENT_NAME "Segment"

using coordinate_t = int;

static std::string bool_repr(bool value) { return py::str(py::bool_(value)); }

template <class Object>
std::string repr(const Object& object) {
  std::ostringstream stream;
  stream.precision(std::numeric_limits<double>::digits10 + 2);
  stream << object;
  return stream.str();
}

static std::ostream& operator<<(std::ostream& stream, const Point& point) {
  return stream << C_STR(MODULE_NAME) "." POINT_NAME "(" << point.X << ", "
                << point.Y << ")";
}

static std::ostream& operator<<(std::ostream& stream, const Segment& segment) {
  return stream << C_STR(MODULE_NAME) "." SEGMENT_NAME "(" << segment.p0 << ", "
                << segment.p1 << ")";
}

static bool operator==(const Point& left, const Point& right) {
  return left.X == right.X && left.Y == right.Y;
}

static bool operator==(const Segment& left, const Segment& right) {
  return left.p0 == right.p0 && left.p1 == right.p1;
}

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(Python binding of Voxel8/pyvoronoi library.)pbdoc";

  py::class_<Point>(m, POINT_NAME)
      .def(py::init<coordinate_t, coordinate_t>(), py::arg("x"), py::arg("y"))
      .def("__repr__", repr<Point>)
      .def(py::self == py::self)
      .def_readonly("x", &Point::X)
      .def_readonly("y", &Point::Y);

  py::class_<Segment>(m, SEGMENT_NAME)
      .def(py::init<Point, Point>(), py::arg("start"), py::arg("end"))
      .def("__repr__", repr<Segment>)
      .def(py::self == py::self)
      .def_readonly("start", &Segment::p0)
      .def_readonly("end", &Segment::p1);

#ifdef VERSION_INFO
  m.attr("__version__") = VERSION_INFO;
#else
  m.attr("__version__") = "dev";
#endif
}
