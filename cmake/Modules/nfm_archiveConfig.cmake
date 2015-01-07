INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_NFM_ARCHIVE nfm_archive)

FIND_PATH(
    NFM_ARCHIVE_INCLUDE_DIRS
    NAMES nfm_archive/api.h
    HINTS $ENV{NFM_ARCHIVE_DIR}/include
        ${PC_NFM_ARCHIVE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    NFM_ARCHIVE_LIBRARIES
    NAMES gnuradio-nfm_archive
    HINTS $ENV{NFM_ARCHIVE_DIR}/lib
        ${PC_NFM_ARCHIVE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(NFM_ARCHIVE DEFAULT_MSG NFM_ARCHIVE_LIBRARIES NFM_ARCHIVE_INCLUDE_DIRS)
MARK_AS_ADVANCED(NFM_ARCHIVE_LIBRARIES NFM_ARCHIVE_INCLUDE_DIRS)

