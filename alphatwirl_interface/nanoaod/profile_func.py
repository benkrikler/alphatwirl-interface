from __future__ import print_function


def profile_func(func, profile_out_path=None):
    import cProfile
    import pstats
    import StringIO
    pr = cProfile.Profile()
    pr.enable()
    result = func()
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).strip_dirs().sort_stats(sortby)
    ps.print_stats()
    if profile_out_path is None:
        print(s.getvalue())
    else:
        with open(profile_out_path, 'w') as f:
            f.write(s.getvalue())
            f.close()
    return result
