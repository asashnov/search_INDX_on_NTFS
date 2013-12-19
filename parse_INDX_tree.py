#!/usr/bin/env python
#
import sys
import tempfile
import subprocess

image_file=""
index_file=""

# Sector size used by './search_INDX' tool.
SEC_SIZE=512

# use 64 on a 64-bit system
WISP="./wisp32"


def args_parse():
    global image_file, index_file

    if len(sys.argv) != 3:
        printf >>sys.stderr, """Error: invalid usage.
Usage: %s <NTFS_disk_image>  <INDX_list>

Where <NTFS_disk_image> is a device file or dd/ddrescue image file and
<INDX_list> is a text file with one number per line with 512 bytes sectors
starting with 'INDX' text (NTFS directory index file)
        """
        return False

    image_file = sys.argv[1]
    index_file = sys.argv[2]
    return True


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
    if args_parse() and sanity_checks():
        do_job()
