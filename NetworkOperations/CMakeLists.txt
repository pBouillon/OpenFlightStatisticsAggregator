cmake_minimum_required(VERSION 3.14)
project(NetworkOperations C)

set(CMAKE_C_STANDARD 99)

add_executable(
        NetworkOperations
        main.c
        client/client.c client/client.h
        server/server.c server/server.h
        dal/dal.c dal/dal.h
        tcp/tcp_errors.h
        log/logger.c log/logger.h
        algorithms/pathfinding/dijkstra.c algorithms/pathfinding/dijkstra.h algorithms/pathfinding/a_star.c algorithms/pathfinding/a_star.h algorithms/structure/graph.c algorithms/structure/graph.h algorithms/algorithms.h algorithms/algorithms.c)

target_link_libraries(NetworkOperations LINK_PUBLIC sqlite3)