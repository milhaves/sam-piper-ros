# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_stowed_goal_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED stowed_goal_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(stowed_goal_FOUND FALSE)
  elseif(NOT stowed_goal_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(stowed_goal_FOUND FALSE)
  endif()
  return()
endif()
set(_stowed_goal_CONFIG_INCLUDED TRUE)

# output package information
if(NOT stowed_goal_FIND_QUIETLY)
  message(STATUS "Found stowed_goal: 0.0.0 (${stowed_goal_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'stowed_goal' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${stowed_goal_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(stowed_goal_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${stowed_goal_DIR}/${_extra}")
endforeach()
