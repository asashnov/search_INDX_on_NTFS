#!/usr/bin/env python
#
import sys
import platform
import tempfile
import subprocess
import argparse



image_file=""
index_file=""

# Sector size used by './search_INDX' tool.
SEC_SIZE=512

# use 64 on a 64-bit system
if platform.machine().endswith('64'):
    WISP="./3rdparty/64/wisp64"
else:
    WISP="./3rdparty/32/wisp32"


def sanity_checks():
    # TODO:
    # <image file is big>
    # <index file is text with number in first line
    # wisp is downloaded into current dir
    return True


class IndexList:
    """ Reading a text file with a number in each line """
    def __init__(self, filename):
        self.fp = open(filename, 'r')
    def __iter__(self):
        return self
    def next(self):
        line = self.fp.readline().strip()
        if len(line):
            return int(line)
        else:
            raise StopIteration


def parse_wisp_output(output_filename):
    print "parse wisp output"
    return


# Gets image file and creates index file for it.
#
def get_index_file(image_file):

    index_file = image_file + ".idx"

    if os.path.exists(index_file):
        return index_file

    helper_exe = "helpers/search_INDX"

    p = subprocess.Popen(
        shell=False,
        args = [ helper_exe, image_file ],
        stdout = subprocess.PIPE
        )

    fp = open(index_file, "w")
    for line in p.stdout:
        fp.write(line)
    fp.close()
    return index_file


def get_csv_for_disk(image_file):

    index_file = get_index_file(image_file)





def do_job():
    f = open(image_file, 'rb')

    for s in IndexList(index_file):

        # read INDX from disk and store to tmp file
        f.seek(s * SEC_SIZE)
        indx = f.read(1024*1024)  # FIXME: I do not know how to detect the end of INDX
        tmp = tempfile.NamedTemporaryFile(prefix="ntfs_indx_")
        tmp.write(indx)
        tmp.flush()

        # Parse record-by-record filling directory tree
        p = subprocess.Popen(
            shell=False,
            args = [ WISP, '-valid', '-csv', '-base10', '-indxfile', tmp.name ],
            stdout = subprocess.PIPE
            )

        for line in p.stdout:
            print line.strip()

        print "----------"


        p.wait()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search and re-construct directories structure from broken NTFS disk image")
    parser.add_argument('--image', help="Disk image file", action='store', dest='image', required=True)
    args = parser.parse_args()

    csvfile = get_csv_for_disk(args.image)

    parse_tree(cvsfile)
