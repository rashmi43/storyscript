# -*- coding: utf-8 -*-


class Lines:
    """
    Holds compiled lines and provides methods for operation on lines.
    """
    def __init__(self):
        self.lines = {}
        self.services = []
        self.functions = {}
        self.outputs = {}

    def sort(self):
        """
        Returns ordered line numbers
        """
        return sorted(self.lines.keys(), key=lambda x: int(x))

    def last(self):
        """
        Gets the last line
        """
        if self.lines:
            return self.sort()[-1]

    def set_next(self, line_number):
        """
        Finds the previous line, and set the current as its next line
        """
        previous_line = self.last()
        if previous_line:
            self.lines[previous_line]['next'] = line_number

    def set_exit(self, line):
        for line_number in self.sort()[::-1]:
            if self.lines[line_number]['method'] in ['if', 'elif']:
                self.lines[line_number]['exit'] = line
                break

    def set_output(self, line, output):
        self.outputs[line] = output

    def is_output(self, parent_line, service):
        """
        Checks whether a service has been defined as output for this block
        """
        if parent_line in self.outputs:
            if service in self.outputs[parent_line]:
                return True
        return False

    def make(self, method, line, args=None, service=None, command=None,
             function=None, output=None, enter=None, exit=None, parent=None):
        """
        Creates the base dictionary for a given line.
        """
        dictionary = {
            line: {
                'method': method,
                'ln': line,
                'output': output,
                'service': service,
                'command': command,
                'function': function,
                'args': args,
                'enter': enter,
                'exit': exit,
                'parent': parent
            }
        }
        self.lines = {**self.lines, **dictionary}

    def append(self, method, line, **kwargs):
        if 'service' in kwargs:
            if kwargs['service'] in self.functions:
                method = 'call'

        if method == 'function':
            self.functions[kwargs['function']] = line
        elif method == 'execute':
            if self.is_output(kwargs['parent'], kwargs['service']) is False:
                self.services.append(kwargs['service'])
        self.set_next(line)
        self.make(method, line, **kwargs)

    def get_services(self):
        """
        Get the services and remove duplicates.
        """
        return list(set(self.services))
