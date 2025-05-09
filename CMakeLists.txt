#The minimum required CMake version
cmake_minimum_required(VERSION 3.25)
#Defining the name of the project, the version, and language permitted.
project(
    GraphicProjectTutorial
    VERSION 1.0.0
    LANGUAGES C CXX
)
#Setting the C and C++ standard.
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 20)
#The CMAKE_C_STANDARD and CMAKE_CXX_STANDARD variables are used to specify the C and C++ standards to be used for the project. The CMAKE_C_STANDARD variable is set to 11, which corresponds to the C11 standard, while the CMAKE_CXX_STANDARD variable is set to 20, which corresponds to the C++20 standard.
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
#The CMAKE_C_EXTENSIONS and CMAKE_C_EXTENSIONS variables controls whether compiler-specific extensions are enabled using a particular C/C++ standards.
set(CMAKE_C_EXTENSIONS ON)
set(CMAKE_CXX_EXTENSIONS ON)
#Setting Github variables for the project and VCPKG
set(VCPKG_REPO_DIR "${CMAKE_SOURCE_DIR}/external/vcpkg")
set(VCPKG_REPO_URL "https://github.com/microsoft/vcpkg.git" CACHE STRING "")
set(VCPKG_BUILDSYSTEMS_CMAKE_FILE "${VCPKG_REPO_DIR}/scripts/buildsystems/vcpkg.cmake" CACHE STRING "")
set(VCPKG_EXE "${VCPKG_REPO_DIR}/vcpkg.exe")
#Set variable name for Library and Executable 
set(LIB_NAME Library)
set(EXE_NAME GraphicsProjectTest)
#Variable for the tools 
set(TOOL_BASE_ADDR "${CMAKE_SOURCE_DIR}/tools")
set(VCPKG_COMMIT_TOOL "${CMAKE_SOURCE_DIR}/tools/vcpkg-commit-getter.py" CACHE STRING "")
#finding the Python3 interpreter
find_package(Python3 COMPONENTS Interpreter REQUIRED)

#Checking if the vcpkg repository already exists
if(NOT EXISTS "${VCPKG_REPO_DIR}/.git")
    message(STATUS "Cloning ${VCPKG_REPO_URL} into ${VCPKG_REPO_DIR}")
    execute_process(
        COMMAND git clone --recursive ${VCPKG_REPO_URL} ${VCPKG_REPO_DIR}
        RESULT_VARIABLE GIT_RESULT
        OUTPUT_VARIABLE GIT_OUTPUT
        ERROR_VARIABLE GIT_ERROR
    )
    if(NOT GIT_RESULT EQUAL 0)
        message(FATAL_ERROR "Failed to clone vcpkg repository: ${GIT_ERROR}")
    endif()
else()
    message(STATUS "${VCPKG_REPO_URL} repository already exists at ${VCPKG_REPO_DIR}")
endif()

# List of options
option(ENABLE_EXECUTABLE "General executable" ON)
option(ENABLE_TESTS "Enable tests" ON)
option(USE_VCPKG "Enable vcpkg" ON)

# Including the vcpkg directory in the CMake module path
if(USE_VCPKG)
    if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
        if(NOT EXISTS "${VCPKG_EXE}")
            message(STATUS "vcpkg not found. Bootstrapping vcpkg in ${VCPKG_REPO_DIR}")
            # Run bootstap scrip (for Windows)
            execute_process(
                COMMAND cmd /c "cd /d ${VCPKG_REPO_DIR} && .\\bootstrap-vcpkg.bat"
                RESULT_VARIABLE BOOTSTRAP_RESULT
                OUTPUT_VARIABLE BOOTSTRAP_OUT    
                ERROR_VARIABLE BOOTSTRAP_ERR
            )
            if(NOT BOOTSTRAP_RESULT EQUAL 0)
                message(FATAL_ERROR "Failed to bootstrap vcpkg: ${BOOTSTRAP_ERR}\n")
            else()
                message(STATUS "vcpkg bootstrapped successfully: ${BOOTSTRAP_OUT}\nBootstrap result: ${BOOTSTRAP_RESULT}")
            endif()
            # Set CMake toolchain file to vcpkg
            set(CMAKE_TOOLCHAIN_FILE "${CMAKE_CURRENT_SOURCE_DIR}/external/vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "")
            
            message(STATUS "Adding vcpkg to PATH")
            set(ENV{PATH} "$ENV{PATH};${VCPKG_REPO_DIR}")
            message(STATUS "New PATH: $ENV{PATH}")
            # Storing the vcpkg git commit hash in a variable
            message(STATUS "Getting VCPKG commit hash using python script found at: ${VCPKG_COMMIT_TOOL}")
            execute_process(
                COMMAND ${Python3_EXECUTABLE} "${VCPKG_COMMIT_TOOL}"
                WORKING_DIRECTORY ${TOOL_BASE_ADDR}
                RESULT_VARIABLE VCPKG_TOOL_RESULT
                OUTPUT_VARIABLE VCPKG_TOOL_OUTPUT
                ERROR_VARIABLE VCPKG_TOOL_ERROR
            )
            if(NOT VCPKG_TOOL_RESULT EQUAL 0)
                message(FATAL_ERROR "Failed to run VCPKG tool script: ${VCPKG_COMMIT_TOOL}\nError: ${VCPKG_TOOL_ERROR}")
            else()
                message(STATUS "Tool executed at: ${VCPKG_COMMIT_TOOL}")
            endif()
        else()
            message(STATUS "vckpg found at ${VCPKG_EXE}")
        endif()
        # include the vcpkg buildsystem
        message(STATUS "Including vcpkg buildsystem")
        include(${VCPKG_BUILDSYSTEMS_CMAKE_FILE})
        # Run the install from the vcpkg json
        execute_process(
            COMMAND cmd /c "${VCPKG_EXE} integrate install"
            RESULT_VARIABLE VCPKG_RESULT
            OUTPUT_VARIABLE VCPKG_OUTPUT
            ERROR_VARIABLE VCPKG_ERROR
        )
        if(NOT VCPKG_RESULT EQUAL 0)
            message(FATAL_ERROR "Failed to run vcpkg install: ${VCPKG_ERROR}")
        else()
            message(STATUS "vcpkg install result: ${VCPKG_OUTPUT}")
        endif()
    endif()
endif()