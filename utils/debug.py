import functools
import time
from django.db import connection, reset_queries
from uuid import uuid4
import tracemalloc
import logging
import functools
import tracemalloc
logger = logging.getLogger(__name__)





def query_debugger(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        tracemalloc.start()

        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        # Log memory usage statistics
        print(
            f"Memory usage: {current / 1024 / 1024:.2f}MB (peak: {peak / 1024 / 1024:.2f}MB)")

        for sql in connection.queries:
            print(sql)
            print("\n\n ")
        return result

    return inner_func
