#!/usr/bin/env python
import os
from l3sdk import define, Process


class SortAndIndex(define.Wrapper):

    class Inputs(define.Inputs):
        bamInput = define.input(name="BAM input", description="input the bwa aligned bam file", required=True)

    class Outputs(define.Outputs):
        bamOutput = define.output(name="BAM output", required=True)

    class Params(define.Params):
        reference = define.string(name="reference",required=True)

    def execute(self):
        out_bam_file = self.Inputs.bamInput
        out_bam_name = os.path.basename(out_bam_file)
        out_bam_name = out_bam_name[::-1].replace(".bam"[::-1], ".sorted.bam"[::-1], 1)[::-1]
        Process("/opt/bin/sort_and_index_v1.py", self.Params.reference, self.Inputs.bamInput, out_bam_name)
        self.Outputs.bamOutput = out_bam_name
        self.Outputs.bamOutput.meta = self.Inputs.bamInput.make_metadata()


def test_sort_and_index():
    pass

if __name__ == "__main__":
    test_sort_and_index()
