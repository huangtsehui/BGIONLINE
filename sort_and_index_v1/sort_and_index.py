#! /usr/bin/env python
import sys
import os
from subprocess import check_call

if len(sys.argv) != 3:
    print "Usage: %s <reference> <bamInput> <bamOutput.sort>"
    sys.exit(1)


def has_build_index(ref_prefix):
    index = glob.glob("%s.*" % ref_prefix)
    if len(index) <= 5:
        return False
    return True



def picard_sort(bam):
    bam_fixmate = bam + ".fixmate"
    cmd =  "/usr/bin/java -Xmx3g -Djava.io.tmpdir=/tmp -XX:MaxPermSize=512m -XX:-UseGCOverheadLimit "
    cmd += "-jar /opt/bin/picard/FixMateInformation.jar"
    cmd += "I=%s" % bam
    cmd += "O=%s" % bam_fixmate
    cmd += "SO=coordinate VALIDATION_STRINGENCY=SILENT"
    check_call(cmd)
    return bam_fixmate


def samtools_sort_index(reference, bam_fixmate, bam_output):
    # out_bam = bam_fixmate.split(".")[:-2] + ".bam"
    check_call("/opt/bin/samtools", "calmd -b",reference, ">", bam_output)
    check_call("/opt/bin/samtools", "index", bam_output)
    return out_bam


if __name__ == "__main__":
    (reference, bam_input, bam_output) = sys.argv[1:]
    reference = os.path.join("/opt/db", reference)
    if not has_build_index(reference):
        sys.exit(1)

    try:
        bam_fixmate = picard_sort(bam_input)
        samtools_sort_index(reference, bam_fixmate, bam_output)
    except Exception,e:
        print str(e)