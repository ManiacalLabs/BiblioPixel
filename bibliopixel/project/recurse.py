from . import aliases, construct

"""
In order to validate project descriptions, we need to recurse through project
dictionaries before we actually construct the objects in them.

Some fields of project dictionaries are designated to be "type constructors" -
i.e. they describe how to create an object.  We need to recurse down through
those - and how we do so depends on the type of the object.

For example, at the top level, the "layout" and "animation" fields are
type constructors while the "run" and "path" fields are not.

So recurse uses static class members on the object class being created
to determine what to do before and after recursion, and how to compute
children.
"""


def recurse(desc, pre='pre_recursion', post='post_recursion',
            children='children', python_path=None):
    """
    Depth first recursion through a dictionary containing type constructors

    The arguments pre, post and children are independently either:

    * None, which means to do nothing
    * a string, which means to use the static class method of that name on the
      class being constructed, or
    * a callable, to be called at each recursion

    Arguments:

    dictionary -- a project dictionary or one of its subdictionaries
    pre -- called before children are visited node in the recursion
    children -- returns a possibly empty list of child nodes for this node
    post -- called after children are visited in the recursion.

    """
    def call(f, desc):
        if isinstance(f, str):
            # f is the name of a static class method on the datatype.
            f = getattr(datatype, f, None)
            return f and f(desc)

        # f is a function.
        return f and f(datatype, desc)

    desc = construct.to_type_constructor(desc, python_path)
    datatype = desc.get('datatype')

    desc = call(pre, desc) or desc

    for key, coll, *new_path in call(children, desc) or ():
        new_path = new_path[0] if new_path else python_path
        coll[key] = recurse(coll[key], pre, post, children, new_path)

    return call(post, desc) or desc
