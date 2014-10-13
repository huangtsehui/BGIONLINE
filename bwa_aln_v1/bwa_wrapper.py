import os
from l3sdk import define, Process


class BwaAlign(define.Wrapper):
    """ this wrapper use bwa to align raw reads, output bam files per sample """

    class Inputs(define.Inputs):
        fq = define.input(name='FASTQ', description='Input a pair of FASTQ file', required=True,list=True)
        # ref = define.Inputs(name="Reference", description="Input a pre-bulid reference index files path",
        #                     required=True, list=False)

    class Outputs(define.Outputs):
        bam = define.output(name='BAM output', required=True,list=False)

    class Params(define.Params):
        sampleName = define.string(name='sample name', required=True)
        reference = define.string(name="reference name", required=True)

    def execute(self):
        out_file_name = "%s.bam" % self.Params.sampleName
        Process('/opt/bin/bwa_aln.py',
                self.Inputs.fq[0], self.Inputs.fq[1],
                self.Params.reference,
                self.Params.sampleName,
                stdout=out_file_name).run()

        self.Outputs.bam = out_file_name
        self.Outputs.bam.meta = self.Inputs.make_metadata()

def test_BwaWrapper():
    inputs = {'fq': ['/l3bioinfo/test-data/1.fq.gz', '/l3bioinfo/test-data/2.fq.gz']}
    params = {'sampleName' : 'TEST'}
    outputs = BwaAlign(inputs, params).test()
    assert outputs.bam.endswith('.bam')

if __name__ == '__main__':
    test_BwaWrapper()
