set(GFLAGS_USE_TARGET_NAMESPACE ON)

set(
    LIB_INCLUDES
    "./Inc/"
    "${_VCPKG_INSTALLED_DIR}/x64-windows/include/"
)

find_package(gflags CONFIG REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 CONFIG REQUIRED)
find_package(glog CONFIG REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLUT REQUIRED)

list(APPEND LIB_SOURCES "window.cpp")
list(APPEND LIB_HEADERS "./inc/window.h")

list(APPEND LINK_LIB gflags::gflags)
list(APPEND LINK_LIB GLEW::GLEW)
list(APPEND LINK_LIBRARIES glfw)
list(APPEND LINK_LIBRARIES glog::glog)
list(APPEND LINK_LIBRARIES OpenGL::GL)
list(APPEND LINK_LIBRARIES GLUT::GLUT)

add_library(${LIB_NAME} STATIC
            ${LIB_SOURCES}
            ${LIB_HEADERS}
)

target_include_directories(${LIB_NAME} PUBLIC ${LIB_INCLUDES})
target_link_libraries(${LIB_NAME} PRIVATE ${LINK_LIB})