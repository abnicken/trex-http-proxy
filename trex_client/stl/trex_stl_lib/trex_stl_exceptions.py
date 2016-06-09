import os
import sys
import linecache

from .utils.text_opts import *

# basic error for API
class STLError(Exception):
    def __init__ (self, msg):
        self.msg = str(msg)

    def __str__ (self):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if not exc_tb:
            return self.msg
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]


        src_line = str(linecache.getline(fname, exc_tb.tb_lineno))


        s = "\n******\n"
        s += "Error at {0}:{1} - '{2}'\n\n".format(format_text(fname, 'bold'), format_text(exc_tb.tb_lineno, 'bold'), format_text(src_line.strip(), 'bold'))
        s += "specific error:\n\n{0}\n".format(format_text(self.msg, 'bold'))

        

        return s

    def brief (self):
        return self.msg


# raised when the client state is invalid for operation
class STLStateError(STLError):
    def __init__ (self, op, state):
        self.msg = "Operation '{0}' is not valid while '{1}'".format(op, state)


# port state error
class STLPortStateError(STLError):
    def __init__ (self, port, op, state):
        self.msg = "Operation '{0}' on port(s) '{1}' is not valid while port(s) '{2}'".format(op, port, state)


# raised when argument value is not valid for operation
class STLArgumentError(STLError):
    def __init__ (self, name, got, valid_values = None, extended = None):
        self.msg = "Argument: '{0}' invalid value: '{1}'".format(name, got)
        if valid_values:
            self.msg += " - valid values are '{0}'".format(valid_values)

        if extended:
            self.msg += "\n{0}".format(extended)

# raised when argument type is not valid for operation
class STLTypeError(STLError):
    def __init__ (self, arg_name, arg_type, valid_types):
        self.msg = "Argument: '%s' invalid type: %s, expecting type(s): %s." % (arg_name, arg_type, valid_types)

# raised when timeout occurs
class STLTimeoutError(STLError):
    def __init__ (self, timeout):
        self.msg = "Timeout: operation took more than '{0}' seconds".format(timeout)


