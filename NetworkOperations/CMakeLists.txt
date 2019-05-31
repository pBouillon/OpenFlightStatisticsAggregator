cmake_minimum_required(VERSION 3.14)
project(NetworkOperations C)

set(CMAKE_C_STANDARD 99)

add_executable(NetworkOperations main.c client/client.c client/client.h server/server.c server/server.h dal/dal.c dal/dal.h tcp/tcp_errors.h)