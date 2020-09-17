// Boost.Polygon library point_concept.hpp header file

// Copyright (c) Intel Corporation 2008.
// Copyright (c) 2008-2012 Simonson Lucanus.
// Copyright (c) 2012-2012 Andrii Sydorchuk.

// See http://www.boost.org for updates, documentation, and revision history.
// Use, modification and distribution is subject to the Boost Software License,
// Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef BOOST_POLYGON_POINT_CONCEPT_HPP
#define BOOST_POLYGON_POINT_CONCEPT_HPP

#include "isotropy.hpp"
#include "point_traits.hpp"

namespace boost {
namespace polygon {

struct point_concept {};

template <typename ConceptType>
struct is_point_concept {
  typedef gtl_no type;
};

template <>
struct is_point_concept<point_concept> {
  typedef gtl_yes type;
};

template <typename GeometryType, typename BoolType>
struct point_coordinate_type_by_concept {
  typedef void type;
};

template <typename GeometryType>
struct point_coordinate_type_by_concept<GeometryType, gtl_yes> {
  typedef typename point_traits<GeometryType>::coordinate_type type;
};

template <typename GeometryType>
struct point_coordinate_type {
  typedef typename point_coordinate_type_by_concept<
      GeometryType, typename is_point_concept<typename geometry_concept<
                        GeometryType>::type>::type>::type type;
};

struct y_pt_get : gtl_yes {};

template <typename PointType>
typename enable_if<
    typename gtl_and<
        y_pt_get, typename is_point_concept<
                      typename geometry_concept<PointType>::type>::type>::type,
    typename point_coordinate_type<PointType>::type>::type
get(const PointType& point, orientation_2d orient) {
  return point_traits<PointType>::get(point, orient);
}

struct y_p_x : gtl_yes {};

template <typename PointType>
typename enable_if<
    typename gtl_and<y_p_x, typename is_point_concept<typename geometry_concept<
                                PointType>::type>::type>::type,
    typename point_coordinate_type<PointType>::type>::type
x(const PointType& point) {
  return get(point, HORIZONTAL);
}

struct y_p_y : gtl_yes {};

template <typename PointType>
typename enable_if<
    typename gtl_and<y_p_y, typename is_point_concept<typename geometry_concept<
                                PointType>::type>::type>::type,
    typename point_coordinate_type<PointType>::type>::type
y(const PointType& point) {
  return get(point, VERTICAL);
}
}  // namespace polygon
}  // namespace boost

#endif  // BOOST_POLYGON_POINT_CONCEPT_HPP
