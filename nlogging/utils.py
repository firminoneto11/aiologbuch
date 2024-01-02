from inspect import isabstract


def is_direct_subclass[T: object, I: object](value: T, base_cls: I):
    if isabstract(value):
        raise TypeError("Abstract classes are not allowed")

    subclasses = [el.__name__ for el in base_cls.__class__.__subclasses__(base_cls)]

    # If 'value' is a class, check if it's name is in the subclasses list
    if value.__class__ is type:
        return value.__name__ in subclasses

    # If 'value' inherits from ABCMeta, check if it's name is in the subclasses list
    if value.__class__.__name__ == "ABCMeta":
        return value.__name__ in subclasses

    # If 'value' is an instance, check if it's class name is in the subclasses list
    return value.__class__.__name__ in subclasses
