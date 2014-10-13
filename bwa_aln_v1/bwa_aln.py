#!/usr/bin/env python
import os
import sys
import glob
import re
from subprocess import check_call

if len(sys.argv) != 4:
    print "Usage: %s <fq1> <fq2> <reference> <sample_name>" % sys.argv[0]


def has_build_index(ref_prefix):
    index = glob.glob("%s.*" % ref_prefix)
    if len(index) <= 5:
        return False
    return True


def bwa_aln(fq_file, reference):
    sai = fq_file
    options = "-o 1 -e 50 -m 100000 -t 4 -i 15 -q 10 -I"
    check_call("/opt/bin/bwa", "aln", options, sai, reference, fq_file)
    # cmd = "/opt/bin/bwa aln %s -f %s %s %s" % (options, sai, reference, fq_file)
    # os.system(cmd)
    return sai


def bwa_sampe(sai_1, sai_2, fq1, fq2, reference ):
    options = ""
    check_call("/opt/bin/baw","sampe", options, reference, sai_1, sai_2, fq1, fq2, "| /opt/bin/samtools view -Sb -T",reference, "-")
    # cmd = "/opt/bin/bwa sampe %s %s %s %s %s %s | /opt/bin/samtools view -Sb -T " % (options, reference, sai_1, sai_2, fq1, fq2 )
    # os.system(cmd)
    return


if __name__ == "__main__":
    (fq1, fq2, reference, sample_name) = sys.argv[1:]
    reference = os.path.join("/opt/db", reference)
    if not has_build_index(reference):
        sys.exit(1)

    try:
        sai_1 = bwa_aln(fq1, reference)
        sai_2 = bwa_aln(fq2, reference)
        bwa_sampe(sai_1, sai_2, fq1, fq2, reference)
    except Exception, e:
        print str(e)








