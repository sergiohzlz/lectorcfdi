import os
import argparse
import glob

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Prueba')
    dir_actual = os.path.dirname(os.path.realpath((__file__)))
    print(f'Dir actual {dir_actual}')
    parser == parser.add_argument('--dir_salida', help='Dir salida') # type: ignore

    args = parser.parse_args()
    dirsalida = args.dir_salida
    print(f"Dir salida {dirsalida}")
    files = glob.glob(os.path.join( dirsalida, '*.xml'))
    print(files)
