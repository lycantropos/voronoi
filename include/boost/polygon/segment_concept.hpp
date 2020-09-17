// Boost.Polygon library segment_concept.hpp header file

// Copyright (c) Intel Corporation 2008.
// Copyright (c) 2008-2012 Simonson Lucanus.
// Copyright (c) 2012-2012 Andrii Sydorchuk.

// See http://www.boost.org for updates, documentation, and revision history.
// Use, modification and distribution is subject to the Boost Software License,
// Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef BOOST_POLYGON_SEGMENT_CONCEPT_HPP
#define BOOST_POLYGON_SEGMENT_CONCEPT_HPP

#include "isotropy.hpp"
#include "segment_traits.hpp"

namespace boost {
namespace polygon {

struct segment_concept {};

template <typename ConceptType>
struct is_segment_concept {
  typedef gtl_no type;
};

template <>
struct is_segment_concept<segment_concept> {
  typedef gtl_yes type;
};

template <typename GeometryType, typename BoolType>
struct segment_point_type_by_concept {
  typedef void type;
};

template <typename GeometryType>
struct segment_point_type_by_concept<GeometryType, gtl_yes> {
  typedef typename segment_traits<GeometryType>::point_type type;
};

template <typename GeometryType>
struct segment_point_type {
  typedef typename segment_point_type_by_concept<
      GeometryType, typename is_segment_concept<typename geometry_concept<
                        GeometryType>::type>::type>::type type;
};

struct y_s_get : gtl_yes {};

template <typename Segment>
typename enable_if<
    typename gtl_and<y_s_get,
                     typename is_segment_concept<
                         typename geometry_concept<Segment>::type>::type>::type,
    typename segment_point_type<Segment>::type>::type
get(const Segment& segment, direction_1d dir) {
  return segment_traits<Segment>::get(segment, dir);
}

struct y_s_low : gtl_yes {};

template <typename Segment>
typename enable_if<
    typename gtl_and<y_s_low,
                     typename is_segment_concept<
                         typename geometry_concept<Segment>::type>::type>::type,
    typename segment_point_type<Segment>::type>::type
low(const Segment& segment) {
  return get(segment, LOW);
}

struct y_s_high : gtl_yes {};

template <typename Segment>
typename enable_if<
    typename gtl_and<y_s_high,
                     typename is_segment_concept<
                         typename geometry_concept<Segment>::type>::type>::type,
    typename segment_point_type<Segment>::type>::type
high(const Segment& segment) {
  return get(segment, HIGH);
}
}  // namespace polygon
}  // namespace boost

#endif  // BOOST_POLYGON_SEGMENT_CONCEPT_HPP
