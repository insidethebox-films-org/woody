import cProfile
import pstats
import io
import time
from contextlib import contextmanager

class AddonProfiler:
    def __init__(self):
        self.profiler = None
        self.is_profiling = False
        
    def start_profiling(self):
        if not self.is_profiling:
            self.profiler = cProfile.Profile()
            self.profiler.enable()
            self.is_profiling = True
            print("🔍 Profiling started...")
    
    def stop_profiling(self, show_results=True, top_n=20):
        if self.is_profiling and self.profiler:
            self.profiler.disable()
            self.is_profiling = False
            
            if show_results:
                self.print_results(top_n)
    
    def print_results(self, top_n=20):
        if not self.profiler:
            print("❌ No profiling data available")
            return
            
        s = io.StringIO()
        ps = pstats.Stats(self.profiler, stream=s)
        
        print("\n" + "="*80)
        print("🚀 ADDON PERFORMANCE PROFILING RESULTS")
        print("="*80)
        
        # Sort by cumulative time
        ps.sort_stats('cumulative')
        ps.print_stats(top_n)
        print(s.getvalue())


addon_profiler = AddonProfiler()

@contextmanager
def profile_section(section_name):
    """Profile a specific section of code"""
    start_time = time.perf_counter()
    print(f"⏱️  Starting: {section_name}")
    try:
        yield
    finally:
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"✅ Completed: {section_name} - {duration:.4f} seconds")
