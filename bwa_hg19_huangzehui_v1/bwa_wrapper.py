import os
from l3sdk import define, Process


class BwaWrapper(define.Wrapper):
    """ this wrapper use bwa to align raw reads, output bam files per sample """

    class Inputs(define.Inputs):
        fq = define.input(name='FASTQ',description='Input a pair of FASTQ file',required=True,list=True)

    class Outputs(define.Outputs):
        bam = define.output(name='BAM output',required=True,list=False)

    class Params(define.Params):
        sampleName = define.string(name='sample name',required=True)

    def execute(self):
        outFileName = "%s.bam" % self.Params.sampleName
        Process('/opt/bin/bwa_aln',self.Inputs.fq[0],self.Inputs.fq[1],self.Params.sampleName,stdout=outFileName).run()
        self.Outputs.bam = outFileName
        self.Outputs.bam.meta = self.Inputs.make_metadata()

    def test_BWAMEM():
        inputs = {'fq': ['/l3bioinfo/test-data/1.fq.gz','/l3bioinfo/test-data/2.fq.gz']}
        params = {'sampleName' : 'TEST'}
        outputs = BWAMEM(inputs, params).test()
        assert outputs.bam.endswith('.bam')


