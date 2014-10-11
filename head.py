import os
from l3sdk import define, Process

class HeadWrapper(define.Wrapper):
        class Inputs(define.Inputs):
                inp = define.input(required=True)

        class Outputs(define.Outputs):
                out = define.output()

        class Params(define.Params):
                lines = define.integer(min=1, required=True)

        def execute(self):
                out_file_name = "%s.out" % self.inputs.inp
                Process('/usr/bin/head', '-%s' % self.params.lines, self.inputs.inp, stdout=out_file_name).run()
                self.outputs.out = out_file_name
                self.outputs.out.meta = self.inputs.inp.make_metadata()

    def test_head():
        inputs = {'inp': 'test.txt'}
        params = {'lines': 3}
        outputs = HeadWrapper(inputs, params).test()
        print outputs.out
        # assert outputs.out.endswith('a very small')
        with open(outputs.out) as fp:
                lines = fp.readlines()
        print lines
        assert len(lines) == 3

test_head()