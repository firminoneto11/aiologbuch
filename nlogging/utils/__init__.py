def is_direct_subclass[T: object, I: object](cls_or_instance: T, base_cls: I):
    subclasses = [el.__name__ for el in base_cls.__class__.__subclasses__()]

    # If 'cls_or_instance' is a class, check if it's in subclasses
    if cls_or_instance.__class__ is type:
        return cls_or_instance.__name__ in subclasses

    # If 'cls_or_instance' is an instance, check if its class is in subclasses
    return cls_or_instance.__class__.__name__ in subclasses
