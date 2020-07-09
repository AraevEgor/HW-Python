from memory_profiler import profile

@profile
def get1(d, k):
    return d[k]
@profile
def set1(d, k, v):
    d[k] = v
@profile
def get2(d, k):
    return d.get(k)
@profile
def set2(d, k, v):
    d.__setitem__(k, v)
    
if __name__ == '__main__':
    t_dict = {'some': 'value'}
    some = 'some'
    get1(t_dict, some)
    get2(t_dict, some)
    set1(t_dict, some, 1)
    set2(t_dict, some, 1)
