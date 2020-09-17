// Boost.Polygon library point_traits.hpp header file

// Copyright (c) Intel Corporation 2008.
// Copyright (c) 2008-2012 Simonson Lucanus.
// Copyright (c) 2012-2012 Andrii Sydorchuk.

// See http://www.boost.org for updates, documentation, and revision history.
// Use, modification and distribution is subject to the Boost Software License,
// Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef BOOST_POLYGON_POINT_TRAITS_HPP
#define BOOST_POLYGON_POINT_TRAITS_HPP

#include "isotropy.hpp"

namespace boost {
namespace polygon {

template <typename PointType>
struct point_traits {
  typedef PointType point_type;
  typedef typename point_type::coordinate_type coordinate_type;

  static coordinate_type get(const point_type& point, orientation_2d orient) {
    return point.get(orient);
  }
};
}  // namespace polygon
}  // namespace boost

#endif  // BOOST_POLYGON_POINT_TRAITS_HPP
