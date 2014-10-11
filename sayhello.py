__author__ = 'huangtsehui'
import os
from l3sdk import define, Process

class Sayhello(define.Wrapper):

    class Inputs(define.Inputs):
        inp = define.input()

    class Outputs(define.Outputs):
        out = define.output()

    class Params(define.Params):
        who = define.string(required=True)
        times = define.integer(min=3,required=True)

    def execute(self):
        out_file_name = "test.o"
        Process('echo', "-n","%s say hello to you %s times" % (self.Params.who,self.Params.times), stdout=out_file_name).run()
        self.outputs.out = out_file_name
        # self.outputs.out.meta = self.inputs.who.make_metadata()


def test_Sayhello():
    inputs = {'inputs':'test.txt'}
    params = {'who':'huangzehui','times':3}
    outputs = Sayhello(inputs, params).test()
    with open(outputs.out) as fp:
        lines = fp.readline()
    print lines

test_Sayhello()