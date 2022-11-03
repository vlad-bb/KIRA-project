import gc


def clean_memory():
    print("Collecting...")
    n = gc.collect()
    print("Number of unreachable objects collected by GC:", n)
    print("Uncollectable garbage:", gc.garbage)
