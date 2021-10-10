import re
import sys
from math import copysign


def main():
    if len(sys.argv) != 2:
        print("Supply input filename!")
        exit(0)
    f_name = sys.argv[1]
    try:
        with open(f_name, 'r') as fh:
            lines = fh.readlines()
            print('Processing input file consisting of %i lines' % len(lines))
            res = process_lines(lines)
            print('Resulting code has %i lines' % len(res))
        with open(make_output_filename(f_name), 'w+') as fh:
            fh.writelines(res)
        print('File has been processed successfully')
    except FileNotFoundError:
        print("File %s not found!" % f_name)


def process_lines(lines):
    result = []
    buffer = None
    loop_start_re = re.compile(r'\s*{\s*startloop\s*}\s*')
    loop_end_re = re.compile(r'\s*{\s*endloop\s*}\s*')
    num_group = r'(-?\d*\.?\d+)'
    params_re = re.compile(r'\s*{\s*from\s+%s\s+to\s+%s\s+step\s+%s\s*}\s*' % (num_group, num_group, num_group))
    is_macro = False
    loop_params = None
    for ln in lines:
        if is_macro:
            if loop_end_re.match(ln):
                is_macro = False
                result += expand_macro(buffer, loop_params)
            else:
                buffer.append(ln)
        else:
            m = params_re.match(ln)
            if m or loop_start_re.match(ln):
                if m:
                    loop_params = extract_loop_params(m)
                is_macro = True
                buffer = []
            else:
                result.append(ln)
    return result


def extract_loop_params(m):
    return tuple((float(x) for x in m.groups()[0:4]))


def expand_macro(buffer, loop_params):
    rng = list(generate_loop_range(loop_params))
    return [s.replace('$', "%.3f" % v) for v in rng for s in buffer]


def generate_loop_range(params):
    tol = 1.0e-7
    (start, end, step) = params
    delta = end - start
    sign = copysign(1, delta)
    step = copysign(step,  delta)
    x = start
    while (x * sign - end * sign) < -tol:
        yield x
        x += step
    yield end


def make_output_filename(f_name):
    dot_idx = f_name.rfind('.')
    if dot_idx != -1:
        f_name = f_name[:dot_idx]
    return f_name + '_mex.gcode'


if __name__ == "__main__":
    main()

