class MockFunctionHelper(object):
    def __init__(self, func):
        self.func = func

    def will_return(self, value):
        setattr(self.func, 'return_value', value)

    def will_cause_side_effect(self, value):
        setattr(self.func, 'side_effect', value)

    def was_called_with(self, expected):
        actual = getattr(self.func, 'call_args_list')
        msg ='Expected %s but actual %s' % (expected, actual) 
        assert expected == actual, msg
             

