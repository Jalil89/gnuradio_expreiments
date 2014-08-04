class Parent:
    def handler(self):
        print 'parent handler'

    def callback(self):
        self.handler()