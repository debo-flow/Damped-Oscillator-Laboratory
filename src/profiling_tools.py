"""
Milestone 19: Profiling Tools
Provides lightweight decorators for measuring wall-clock time and cProfile statistics.
"""

import time
import cProfile
import pstats
import io
from functools import wraps

def time_it(func):
    """Decorator to measure wall-clock execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[Profiler] {func.__name__} executed in {end - start:.4f} seconds.")
        return result
    return wrapper

def profile_it(func):
    """Decorator to run cProfile on a function and print the top 10 bottlenecks."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
        ps.print_stats(10)
        print(f"\n--- cProfile Results for {func.__name__} ---")
        print(s.getvalue())
        return result
    return wrapper
