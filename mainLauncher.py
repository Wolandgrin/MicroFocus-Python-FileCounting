#!/usr/bin/python
import collections
import getopt
import ntpath
import os
import pathlib
import sys


def main(argv):
    log_dir = pathlib.Path(__file__).parent.absolute()
    log_file = os.path.join(log_dir, 'output.log')
    input_dir = ''

    try:
        opts, args = getopt.getopt(argv, "hp:", ["path="])
    except getopt.GetoptError:
        print('mainLauncher.py -p <directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('mainLauncher.py -p <directory>')
            sys.exit()
        elif opt in ("-p", "--path"):
            input_dir = arg
    if os.path.isdir(input_dir):
        os.chdir(input_dir)
    else:
        print('Directory {} does not exist'.format(input_dir))
        sys.exit()

    text_collector = collections.UserDict()
    ext_counter = collections.Counter()
    total_count = 0
    failed = 0

    for path, dirs, files in os.walk(input_dir):
        total_count += len(files)
        for filename in files:
            name, ext = os.path.splitext(filename)
            # counting files by extension
            ext_counter[ext] += 1
            try:
                with open(os.path.join(path, filename), "r+") as file:
                    for last_line in file:
                        pass
                    st = ntpath.basename(filename)
                    # collecting filename and its last line
                    text_collector[st] = last_line[:-1] if last_line.endswith('\n') else last_line
            except IOError as e:
                print('Unable to open {0} file due to error: {1}'.format(filename, e))
                failed += 1
                continue
            except UnicodeDecodeError as e:
                print('Unable to decode {0} file due to error: {1}'.format(filename, e))
                failed += 1
                continue
            except UnboundLocalError as e:
                print('Unbound error for {0} file due to error: {1}'.format(filename, e))
                failed += 1
                continue
    print('Total number of files in {0}: {1}'.format(input_dir, total_count))
    print('Failed to read last line for {} files'.format(failed))

    print('Following extensions were discovered:')
    for ext, count in ext_counter.most_common():
        if ext == '':
            print("Files without extension:", count)
        else:
            print("'{0}': {1} {2}".format(ext, count, "occurrence" if count == 1 else "occurrences"))

    try:
        os.chdir(log_dir)
        if os.path.isfile(log_file):
            os.remove(log_file)

        with open('output.log', "w+") as file:
            for key, value in text_collector.items():
                file.write("{0}: '{1}'\r\n".format(key, value))
        print('Log file {} successfully created'.format(log_file))
    except IOError as e:
        print('Failed to write to {0} due to {1}'.format(log_file, e))


if __name__ == "__main__":
    main(sys.argv[1:])
