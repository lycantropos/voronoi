/*
  Copyright 2008 Intel Corporation

  Use, modification and distribution are subject to the Boost Software License,
  Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
  http://www.boost.org/LICENSE_1_0.txt).
*/

#ifndef BOOST_POLYGON_ISOTROPY_HPP
#define BOOST_POLYGON_ISOTROPY_HPP

// external
#include <cmath>
#include <cstddef>
#include <cstdlib>
#include <deque>
#include <list>
#include <map>
#include <set>
#include <vector>
//#include <iostream>
#include <algorithm>
#include <iterator>
#include <limits>
#include <string>

#ifndef BOOST_POLYGON_NO_DEPS

#include <boost/config.hpp>
#ifdef BOOST_MSVC
#define BOOST_POLYGON_MSVC
#endif
#ifdef BOOST_INTEL
#define BOOST_POLYGON_ICC
#endif
#ifdef BOOST_HAS_LONG_LONG
#define BOOST_POLYGON_USE_LONG_LONG
typedef boost::long_long_type polygon_long_long_type;
typedef boost::ulong_long_type polygon_ulong_long_type;
// typedef long long polygon_long_long_type;
// typedef unsigned long long polygon_ulong_long_type;
#endif
#include <boost/mpl/and.hpp>
#include <boost/mpl/bool.hpp>
#include <boost/mpl/or.hpp>
#include <boost/mpl/protect.hpp>
#include <boost/mpl/size_t.hpp>
#include <boost/utility/enable_if.hpp>
#else

#ifdef _WIN32
#define BOOST_POLYGON_MSVC
#endif
#ifdef __ICC
#define BOOST_POLYGON_ICC
#endif
#define BOOST_POLYGON_USE_LONG_LONG
typedef long long polygon_long_long_type;
typedef unsigned long long polygon_ulong_long_type;

namespace boost {
template <bool B, class T = void>
struct enable_if_c {
  typedef T type;
};

template <class T>
struct enable_if_c<false, T> {};

template <class Cond, class T = void>
struct enable_if : public enable_if_c<Cond::value, T> {};

template <bool B, class T>
struct lazy_enable_if_c {
  typedef typename T::type type;
};

template <class T>
struct lazy_enable_if_c<false, T> {};

template <class Cond, class T>
struct lazy_enable_if : public lazy_enable_if_c<Cond::value, T> {};

template <bool B, class T = void>
struct disable_if_c {
  typedef T type;
};

template <class T>
struct disable_if_c<true, T> {};

template <class Cond, class T = void>
struct disable_if : public disable_if_c<Cond::value, T> {};

template <bool B, class T>
struct lazy_disable_if_c {
  typedef typename T::type type;
};

template <class T>
struct lazy_disable_if_c<true, T> {};

template <class Cond, class T>
struct lazy_disable_if : public lazy_disable_if_c<Cond::value, T> {};
}  // namespace boost

#endif

namespace boost {
namespace polygon {

struct undefined_concept {};

template <typename T>
struct geometry_concept {
  typedef undefined_concept type;
};

template <typename T>
struct coordinate_traits {};

template <>
struct coordinate_traits<int> {
  typedef int coordinate_type;
  typedef long double area_type;
#ifdef BOOST_POLYGON_USE_LONG_LONG
  typedef polygon_long_long_type manhattan_area_type;
  typedef polygon_ulong_long_type unsigned_area_type;
  typedef polygon_long_long_type coordinate_difference;
#else
  typedef long manhattan_area_type;
  typedef unsigned long unsigned_area_type;
  typedef long coordinate_difference;
#endif
  typedef long double coordinate_distance;
};

#ifdef BOOST_POLYGON_USE_LONG_LONG
template <>
struct coordinate_traits<polygon_long_long_type> {
  typedef polygon_long_long_type coordinate_type;
  typedef long double area_type;
  typedef polygon_long_long_type manhattan_area_type;
  typedef polygon_ulong_long_type unsigned_area_type;
  typedef polygon_long_long_type coordinate_difference;
  typedef long double coordinate_distance;
};
#endif

template <>
struct coordinate_traits<float> {
  typedef float coordinate_type;
  typedef float area_type;
  typedef float manhattan_area_type;
  typedef float unsigned_area_type;
  typedef float coordinate_difference;
  typedef float coordinate_distance;
};

template <>
struct coordinate_traits<double> {
  typedef double coordinate_type;
  typedef double area_type;
  typedef double manhattan_area_type;
  typedef double unsigned_area_type;
  typedef double coordinate_difference;
  typedef double coordinate_distance;
};

template <>
struct coordinate_traits<long double> {
  typedef long double coordinate_type;
  typedef long double area_type;
  typedef long double manhattan_area_type;
  typedef long double unsigned_area_type;
  typedef long double coordinate_difference;
  typedef long double coordinate_distance;
};

struct coordinate_concept {};

template <>
struct geometry_concept<int> {
  typedef coordinate_concept type;
};
#ifdef BOOST_POLYGON_USE_LONG_LONG
template <>
struct geometry_concept<polygon_long_long_type> {
  typedef coordinate_concept type;
};
#endif
template <>
struct geometry_concept<float> {
  typedef coordinate_concept type;
};
template <>
struct geometry_concept<double> {
  typedef coordinate_concept type;
};
template <>
struct geometry_concept<long double> {
  typedef coordinate_concept type;
};

#ifndef BOOST_POLYGON_NO_DEPS
struct gtl_no : mpl::bool_<false> {};
struct gtl_yes : mpl::bool_<true> {};
template <typename T, typename T2>
struct gtl_and : mpl::and_<T, T2> {};
template <typename T, typename T2, typename T3>
struct gtl_and_3 : mpl::and_<T, T2, T3> {};
template <typename T, typename T2, typename T3, typename T4>
struct gtl_and_4 : mpl::and_<T, T2, T3, T4> {};
//  template <typename T, typename T2>
//  struct gtl_or : mpl::or_<T, T2> {};
//  template <typename T, typename T2, typename T3>
//  struct gtl_or_3 : mpl::or_<T, T2, T3> {};
//  template <typename T, typename T2, typename T3, typename T4>
//  struct gtl_or_4 : mpl::or_<T, T2, T3, T4> {};
#else
struct gtl_no {
  static const bool value = false;
};
struct gtl_yes {
  typedef gtl_yes type;
  static const bool value = true;
};

template <bool T, bool T2>
struct gtl_and_c {
  typedef gtl_no type;
};
template <>
struct gtl_and_c<true, true> {
  typedef gtl_yes type;
};

template <typename T, typename T2>
struct gtl_and : gtl_and_c<T::value, T2::value> {};
template <typename T, typename T2, typename T3>
struct gtl_and_3 {
  typedef typename gtl_and<T, typename gtl_and<T2, T3>::type>::type type;
};

template <typename T, typename T2, typename T3, typename T4>
struct gtl_and_4 {
  typedef typename gtl_and_3<T, T2, typename gtl_and<T3, T4>::type>::type type;
};
#endif
template <typename T, typename T2>
struct gtl_or {
  typedef gtl_yes type;
};
template <typename T>
struct gtl_or<T, T> {
  typedef T type;
};

template <typename T, typename T2, typename T3>
struct gtl_or_3 {
  typedef typename gtl_or<T, typename gtl_or<T2, T3>::type>::type type;
};

template <typename T, typename T2, typename T3, typename T4>
struct gtl_or_4 {
  typedef typename gtl_or<T, typename gtl_or_3<T2, T3, T4>::type>::type type;
};

template <typename T>
struct gtl_not {
  typedef gtl_no type;
};
template <>
struct gtl_not<gtl_no> {
  typedef gtl_yes type;
};

template <typename T>
struct gtl_if {
#ifdef BOOST_POLYGON_MSVC
  typedef gtl_no type;
#endif
};
template <>
struct gtl_if<gtl_yes> {
  typedef gtl_yes type;
};

template <typename T, typename T2>
struct gtl_same_type {
  typedef gtl_no type;
};
template <typename T>
struct gtl_same_type<T, T> {
  typedef gtl_yes type;
};
template <typename T, typename T2>
struct gtl_different_type {
  typedef typename gtl_not<typename gtl_same_type<T, T2>::type>::type type;
};

enum direction_1d_enum {
  LOW = 0,
  HIGH = 1,
  LEFT = 0,
  RIGHT = 1,
  CLOCKWISE = 0,
  COUNTERCLOCKWISE = 1,
  REVERSE = 0,
  FORWARD = 1,
  NEGATIVE = 0,
  POSITIVE = 1
};
enum orientation_2d_enum { HORIZONTAL = 0, VERTICAL = 1 };
enum direction_2d_enum { WEST = 0, EAST = 1, SOUTH = 2, NORTH = 3 };

class direction_2d;
class orientation_2d;

class direction_1d {
 private:
  unsigned int val_;
  explicit direction_1d(int d);

 public:
  inline direction_1d() : val_(LOW) {}
  inline direction_1d(const direction_1d& that) : val_(that.val_) {}
  inline direction_1d(const direction_1d_enum val) : val_(val) {}
  explicit inline direction_1d(const direction_2d& that);
  inline direction_1d& operator=(const direction_1d& d) {
    val_ = d.val_;
    return *this;
  }
  inline bool operator==(direction_1d d) const { return (val_ == d.val_); }
  inline bool operator!=(direction_1d d) const { return !((*this) == d); }
  inline unsigned int to_int(void) const { return val_; }
  inline direction_1d& backward() {
    val_ ^= 1;
    return *this;
  }
  inline int get_sign() const { return val_ * 2 - 1; }
};

class direction_2d;

class orientation_2d {
 private:
  unsigned int val_;
  explicit inline orientation_2d(int o);

 public:
  inline orientation_2d() : val_(HORIZONTAL) {}
  inline orientation_2d(const orientation_2d& ori) : val_(ori.val_) {}
  inline orientation_2d(const orientation_2d_enum val) : val_(val) {}
  explicit inline orientation_2d(const direction_2d& that);
  inline orientation_2d& operator=(const orientation_2d& ori) {
    val_ = ori.val_;
    return *this;
  }
  inline bool operator==(orientation_2d that) const {
    return (val_ == that.val_);
  }
  inline bool operator!=(orientation_2d that) const {
    return (val_ != that.val_);
  }
  inline unsigned int to_int() const { return (val_); }
  inline void turn_90() { val_ = val_ ^ 1; }
  inline orientation_2d get_perpendicular() const {
    orientation_2d retval = *this;
    retval.turn_90();
    return retval;
  }
  inline direction_2d get_direction(direction_1d dir) const;
};

class direction_2d {
 private:
  int val_;

 public:
  inline direction_2d() : val_(WEST) {}

  inline direction_2d(const direction_2d& that) : val_(that.val_) {}

  inline direction_2d(const direction_2d_enum val) : val_(val) {}

  inline direction_2d& operator=(const direction_2d& d) {
    val_ = d.val_;
    return *this;
  }

  inline ~direction_2d() {}

  inline bool operator==(direction_2d d) const { return (val_ == d.val_); }
  inline bool operator!=(direction_2d d) const { return !((*this) == d); }
  inline bool operator<(direction_2d d) const { return (val_ < d.val_); }
  inline bool operator<=(direction_2d d) const { return (val_ <= d.val_); }
  inline bool operator>(direction_2d d) const { return (val_ > d.val_); }
  inline bool operator>=(direction_2d d) const { return (val_ >= d.val_); }

  // Casting to int
  inline unsigned int to_int(void) const { return val_; }

  inline direction_2d backward() const {
    // flip the LSB, toggles 0 - 1   and 2 - 3
    return direction_2d(direction_2d_enum(val_ ^ 1));
  }

  // Returns a direction 90 degree left (LOW) or right(HIGH) to this one
  inline direction_2d turn(direction_1d t) const {
    return direction_2d(direction_2d_enum(val_ ^ 3 ^ (val_ >> 1) ^ t.to_int()));
  }

  // Returns a direction 90 degree left to this one
  inline direction_2d left() const { return turn(HIGH); }

  // Returns a direction 90 degree right to this one
  inline direction_2d right() const { return turn(LOW); }

  // N, E are positive, S, W are negative
  inline bool is_positive() const { return (val_ & 1); }
  inline bool is_negative() const { return !is_positive(); }
  inline int get_sign() const { return ((is_positive()) << 1) - 1; }
};

direction_1d::direction_1d(const direction_2d& that)
    : val_(that.to_int() & 1) {}

orientation_2d::orientation_2d(const direction_2d& that)
    : val_(that.to_int() >> 1) {}

direction_2d orientation_2d::get_direction(direction_1d dir) const {
  return direction_2d(direction_2d_enum((val_ << 1) + dir.to_int()));
}
}  // namespace polygon
}  // namespace boost
#endif
