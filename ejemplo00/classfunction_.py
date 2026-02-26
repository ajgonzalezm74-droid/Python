class function:
    # __annotations__ on a function object is already a
    # "data descriptor" in Python, we're just changing
    # what it does
    @property
    def __annotations__(self):
        return self.__annotate__()

# ...

def annotate_foo():
    return {'x': int, 'y': MyType, 'return': float}
def foo(x = 3, y = "abc"):
    ...
foo.__annotate__ = annotate_foo
class MyType:
   ...
foo_y_annotation = foo.__annotations__['y']