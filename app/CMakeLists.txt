set(EXE_APP "app.cpp")

add_executable(${EXE_NAME} ${EXE_APP}) 

target_link_libraries(${EXE_NAME} PRIVATE ${LIB_NAME})