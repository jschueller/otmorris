cmake_minimum_required (VERSION 3.2)

option (BUILD_PYTHON                 "Build the python module for the library"                               ON)
option (USE_SPHINX                   "Use sphinx for documentation"                                          ON)
option (BUILD_SHARED_LIBS            "Build shared libraries"                                                ON)

# By default, build in Release mode. Must appear before project() command
if ( NOT DEFINED CMAKE_BUILD_TYPE )
   set( CMAKE_BUILD_TYPE Release CACHE STRING "Build type")
endif ()

project (OTMORRIS)

string ( TOLOWER ${CMAKE_PROJECT_NAME} PACKAGE_NAME )

# set module dir to find custom scripts
list ( APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake )

find_package (OpenTURNS CONFIG REQUIRED)
message (STATUS "Found OpenTURNS: ${OPENTURNS_ROOT_DIR} (found version \"${OPENTURNS_VERSION_STRING}\")")
set ( OTMORRIS_DEFINITIONS ${OPENTURNS_DEFINITIONS} )
if (NOT BUILD_SHARED_LIBS)
  list ( APPEND OTMORRIS_DEFINITIONS "-DOTMORRIS_STATIC" )
endif ()
add_definitions ( ${OTMORRIS_DEFINITIONS} )

set ( OTMORRIS_LIBRARY_PATH lib${LIB_SUFFIX} )
set ( OTMORRIS_INCLUDE_PATH include)
set ( OTMORRIS_SWIG_INCLUDE_DIRS ${OTMORRIS_INCLUDE_PATH}/${PACKAGE_NAME}/swig )
set ( OTMORRIS_DATA_PATH share )
set ( OTMORRIS_CONFIG_CMAKE_PATH lib${LIB_SUFFIX}/cmake/otmorris )
set (OTMORRIS_DOC_PATH share/${PACKAGE_NAME}/doc)

set (CMAKE_CXX_STANDARD 11)

if (BUILD_PYTHON)
  find_package (SWIG 3)

  find_package (PythonInterp)
  find_package (PythonLibs ${PYTHON_VERSION_STRING} EXACT)
  include (FindPythonModule)
  find_python_module (matplotlib 1.1)

  if (USE_SPHINX)
    find_program (SPHINX_EXECUTABLE NAMES sphinx-build DOC "Sphinx Documentation Builder (sphinx-doc.org)")
    find_python_module (numpydoc)
    if (SPHINX_EXECUTABLE AND NUMPYDOC_FOUND)
      find_python_module (sphinx 1.1)
    endif ()
    if (NOT SPHINX_FOUND)
      message (STATUS "Disabling documentation (need sphinx/pandoc/numpydoc)")
    endif ()
  endif ()

  if (PYTHONINTERP_FOUND)
    if (DEFINED PYTHON_SITE_PACKAGES)
      set (OTMORRIS_PYTHON_MODULE_PATH ${PYTHON_SITE_PACKAGES})

    else ()
      execute_process ( COMMAND ${PYTHON_EXECUTABLE} -c "from distutils import sysconfig; print(sysconfig.get_python_lib(plat_specific=True, prefix='${CMAKE_INSTALL_PREFIX}'))"
                        OUTPUT_VARIABLE _ABS_PYTHON_MODULE_PATH
                        RESULT_VARIABLE _PYTHON_pythonlib_result
                        OUTPUT_STRIP_TRAILING_WHITESPACE )

      if (_PYTHON_pythonlib_result)
        message (SEND_ERROR "Could not run ${PYTHON_EXECUTABLE}")
      endif ()

      get_filename_component (_ABS_PYTHON_MODULE_PATH ${_ABS_PYTHON_MODULE_PATH} ABSOLUTE)
      file (RELATIVE_PATH OTMORRIS_PYTHON_MODULE_PATH ${CMAKE_INSTALL_PREFIX} ${_ABS_PYTHON_MODULE_PATH})
    endif ()

    if (IS_ABSOLUTE ${OTMORRIS_PYTHON_MODULE_PATH})
      set (PYTHON_MODULE_PATH ${OTMORRIS_PYTHON_MODULE_PATH})
    else ()
      set (PYTHON_MODULE_PATH ${CMAKE_INSTALL_PREFIX}/${OTMORRIS_PYTHON_MODULE_PATH})
    endif ()

    set (OTMORRIS_PYTHON${PYTHON_VERSION_MAJOR}_MODULE_PATH ${OTMORRIS_PYTHON_MODULE_PATH})
  endif ( PYTHONINTERP_FOUND )
endif ()


# Define variables without OTMORRIS_ prefix with absolute paths
foreach (_var PYTHON_MODULE_PATH LIBRARY_PATH INCLUDE_PATH CONFIG_CMAKE_PATH)
  if (IS_ABSOLUTE "${OTMORRIS_${_var}}")
    set (${_var} ${OTMORRIS_${_var}})
  else ()
    set (${_var} ${CMAKE_INSTALL_PREFIX}/${OTMORRIS_${_var}})
  endif ()
  get_filename_component (${_var} "${${_var}}" ABSOLUTE)
  file (TO_NATIVE_PATH "${${_var}}" NATIVE_${_var})
  string (REPLACE "\\" "\\\\" NATIVE_${_var} ${NATIVE_${_var}})
endforeach ()

# RPATH settings
set (CMAKE_INSTALL_RPATH ${LIBRARY_PATH})
set (CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
if (POLICY CMP0042)
  # MACOSX_RPATH is enabled by default
  cmake_policy(SET CMP0042 NEW)
endif()
if (POLICY CMP0078)
  # UseSWIG generates standard target names
  cmake_policy(SET CMP0078 NEW)
endif()
if (POLICY CMP0086)
  # UseSWIG honors SWIG_MODULE_NAME via -module flag
  cmake_policy(SET CMP0086 NEW)
endif()

# Some useful macros to ease CMakeLists.txt file writing
set ( SOURCEFILES "" CACHE INTERNAL "List of source files to compile" )
macro ( ot_add_source_file FILENAME )
  set ( sf ${SOURCEFILES} ${CMAKE_CURRENT_SOURCE_DIR}/${FILENAME} )
  set ( SOURCEFILES ${sf} CACHE INTERNAL "List of source files to compile" )
endmacro ( ot_add_source_file )

set ( HEADERFILES "" CACHE INTERNAL "List of header files to install" )
macro ( ot_install_header_file FILENAME )
  set ( hf ${HEADERFILES} ${CMAKE_CURRENT_SOURCE_DIR}/${PACKAGE_NAME}/${FILENAME} )
  set ( HEADERFILES ${hf} CACHE INTERNAL "List of header files to install" )
endmacro ( ot_install_header_file )

set ( SWIGFILES "" CACHE INTERNAL "List of SWIG files to install" )
macro ( ot_install_swig_file FILENAME )
  set ( hf ${SWIGFILES} ${CMAKE_CURRENT_SOURCE_DIR}/${FILENAME} )
  set ( SWIGFILES ${hf} CACHE INTERNAL "List of SWIG files to install" )
endmacro ( ot_install_swig_file )

set ( INTERNAL_INCLUDE_DIRS "" CACHE INTERNAL "List of directories with header files needed for build" )
macro ( ot_add_current_dir_to_include_dirs )
  set ( inc_dirs ${INTERNAL_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR} )
  set ( INTERNAL_INCLUDE_DIRS ${inc_dirs} CACHE INTERNAL "List of directories with header files needed for build" )
endmacro ( ot_add_current_dir_to_include_dirs )


set ( CPACK_PACKAGE_NAME          ${PACKAGE_NAME} )
set ( CPACK_PACKAGE_VERSION_MAJOR 0              )
set ( CPACK_PACKAGE_VERSION_MINOR 9              )
set ( CPACK_PACKAGE_VERSION_PATCH                )
set ( CPACK_SOURCE_GENERATOR      "TGZ;TBZ2"     )
set (CPACK_BINARY_STGZ    OFF CACHE BOOL "STGZ")
set (CPACK_BINARY_TBZ2    ON  CACHE BOOL "TBZ2")
set (CPACK_BINARY_TGZ     ON  CACHE BOOL "TGZ" )
set (CPACK_BINARY_TZ      OFF CACHE BOOL "TZ"  )
set ( CPACK_SOURCE_IGNORE_FILES "/.git;/build;.*~;${CPACK_SOURCE_IGNORE_FILES}" )
set ( PACKAGE_NAME           ${CPACK_PACKAGE_NAME} )
set ( PACKAGE_VERSION        ${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR} )
if ( CPACK_PACKAGE_VERSION_PATCH )
  set ( PACKAGE_VERSION       ${PACKAGE_VERSION}.${CPACK_PACKAGE_VERSION_PATCH} )
endif ()
set ( CPACK_SOURCE_PACKAGE_FILE_NAME ${PACKAGE_NAME}-${PACKAGE_VERSION} )


# The tests can't be run if this function is absent
enable_testing ()
add_custom_target (tests COMMENT "Build tests")
add_custom_target (check COMMENT "Run pre-installation tests")
add_custom_target (installcheck COMMENT "Run post-installation tests")

add_subdirectory (lib)
add_dependencies (check cppcheck)

if (PYTHONINTERP_FOUND AND PYTHONLIBS_FOUND AND SWIG_FOUND)
  add_subdirectory (python)
  add_dependencies (installcheck pyinstallcheck)
endif ()


# uninstall target
configure_file (
  ${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
  IMMEDIATE @ONLY
)

add_custom_target ( uninstall
  COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
)

set ( OTMORRIS_LIBRARY                 otmorris )
set ( OTMORRIS_LIBRARIES ${OPENTURNS_LIBRARIES} )
list ( APPEND OTMORRIS_LIBRARIES ${OTMORRIS_LIBRARY} )
set ( OTMORRIS_LIBRARY_DIRS ${OPENTURNS_LIBRARY_DIRS} )
list ( APPEND OTMORRIS_LIBRARY_DIRS ${LIBRARY_PATH} )
set ( OTMORRIS_INCLUDE_DIR ${INCLUDE_PATH} )
set ( OTMORRIS_INCLUDE_DIRS ${OTMORRIS_INCLUDE_DIR} )
set ( OTMORRIS_ROOT_DIR       ${CMAKE_INSTALL_PREFIX} )
list ( APPEND OTMORRIS_INCLUDE_DIRS ${OPENTURNS_INCLUDE_DIRS} )
set ( OTMORRIS_VERSION_STRING ${PACKAGE_VERSION} )
set ( OTMORRIS_VERSION_MAJOR ${CPACK_PACKAGE_VERSION_MAJOR} )
set ( OTMORRIS_VERSION_MINOR ${CPACK_PACKAGE_VERSION_MINOR} )
set ( OTMORRIS_VERSION_PATCH ${CPACK_PACKAGE_VERSION_PATCH} )
set ( OTMORRIS_USE_FILE      ${CONFIG_CMAKE_PATH}/UseOTMORRIS.cmake )

include(CMakePackageConfigHelpers)
configure_package_config_file (cmake/OTMORRISConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/OTMORRISConfig.cmake
  INSTALL_DESTINATION ${OTMORRIS_CONFIG_CMAKE_PATH}
  PATH_VARS
    OTMORRIS_USE_FILE
    OTMORRIS_ROOT_DIR
    OTMORRIS_INCLUDE_DIR
    OTMORRIS_INCLUDE_DIRS
    OTMORRIS_LIBRARY_DIRS
    PYTHON_MODULE_PATH
  NO_CHECK_REQUIRED_COMPONENTS_MACRO)

write_basic_package_version_file (OTMORRISConfigVersion.cmake VERSION ${OTMORRIS_VERSION_STRING} COMPATIBILITY AnyNewerVersion)

install (FILES cmake/UseOTMORRIS.cmake
               ${CMAKE_CURRENT_BINARY_DIR}/OTMORRISConfig.cmake
               ${CMAKE_CURRENT_BINARY_DIR}/OTMORRISConfigVersion.cmake
         DESTINATION ${OTMORRIS_CONFIG_CMAKE_PATH})

include (CPack)
