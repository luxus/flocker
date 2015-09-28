# Copyright ClusterHQ Inc.  See LICENSE file for details.

"""
Some interface-related tools.
"""

from zope.interface.interface import Method


def interface_decorator(decorator_name, interface, method_decorator,
                        *args, **kwargs):
    """
    Create a class decorator which applies a method decorator to each method of
    an interface.

    Sample Usage::
        class IDummy(Interface):
            def return_method():
                pass

        @implementer(IDummy)
        class Dummy():
            def return_method(self):
                pass

        def method_decorator(method_name, original_name):
            def _run_with_logging(self, *a, **kw):
                Log()
                original_self = getattr(self, original_name)
                return getattr(original_self, method_name)(*a, **kw)
            return _run_with_logging

        def auto_logging(interface, original_name):
            return interface_decorator(
                "auto_logging", IDummy, method_decorator, original,
        )

    :param str decorator_name: A human-meaningful name for the class decorator
        that will be returned by this function.
    :param zope.interface.InterfaceClass interface: The interface from which to
        take methods.
    :param method_decorator: A callable which will decorate a method from the
        interface.  It will be called with the name of the method as the first
        argument and any additional positional and keyword arguments passed to
        ``_interface_decorator``.

    :return: The class decorator.
    """
    for method_name in interface.names():
        if not isinstance(interface[method_name], Method):
            raise TypeError(
                "{} does not support interfaces with non-methods "
                "attributes".format(decorator_name)
            )

    def class_decorator(cls):
        for name in interface.names():
            setattr(cls, name, method_decorator(name, *args, **kwargs))
        return cls
    return class_decorator
