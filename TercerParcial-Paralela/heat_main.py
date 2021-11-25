from __future__ import print_function
import time
import argparse

from heat import init_fields, write_field, iterate
try:
    from heat_cyt import init_fields as init_fields_cyt
    from heat_cyt import write_field as write_field_cyt
    from heat_cyt import iterate as iterate_cyt
except ImportError:
    pass


def main(version='py', input_file='bottle.dat', a=0.5, dx=0.1, dy=0.1, 
         timesteps=200, image_interval=4000):

    if version == 'py':
        #print("Using pure Python")
        init_fields_func = init_fields
        write_field_func = write_field
        iterate_func = iterate
    elif version == 'cyt': 
        #print("Using Cython")
        try:
            init_fields_func = init_fields_cyt
            write_field_func = write_field_cyt
            iterate_func = iterate_cyt
        except NameError as ex:
            raise RuntimeError("Cython extension missing") from ex
    else:
        raise RuntimeError("Unknown version")

    # Initialise the temperature field
    field, field0 = init_fields_func(input_file)

    '''print("Heat equation solver")
    print("Diffusion constant: {}".format(a))
    print("Input file: {}".format(input_file))
    print("Parameters")
    print("----------")
    print("  nx={} ny={} dx={} dy={}".format(field.shape[0], field.shape[1],
                                             dx, dy))
    print("  time steps={}  image interval={}".format(timesteps,
                                                         image_interval))'''

    # Plot/save initial field
    write_field_func(field, 0)
    # Iterate
    t0 = time.time()
    iterate_func(field, field0, a, dx, dy, timesteps, image_interval)
    t1 = time.time()
    # Plot/save final field
    write_field_func(field, timesteps)

    #print("Simulation finished in {0} s".format(t1-t0))
    print(t1-t0)

if __name__ == '__main__':

    # Process command line arguments
    parser = argparse.ArgumentParser(description='Heat equation')
    parser.add_argument('-v', type=str, default='py',
                        help='version')
    parser.add_argument('-dx', type=float, default=0.01,
                        help='grid spacing in x-direction')
    parser.add_argument('-dy', type=float, default=0.01,
                        help='grid spacing in y-direction')
    parser.add_argument('-a', type=float, default=0.5,
                        help='diffusion constant')
    parser.add_argument('-n', type=int, default=200,
                        help='number of time steps')
    parser.add_argument('-i', type=int, default=4000,
                        help='image interval')
    parser.add_argument('-f', type=str, default='bottle.dat', 
                        help='input file')

    args = parser.parse_args()

    main(args.v, args.f, args.a, args.dx, args.dy, args.n, args.i)

