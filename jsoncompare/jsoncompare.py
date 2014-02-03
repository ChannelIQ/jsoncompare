import json
from pprint import pprint

class Stack:
    def __init__(self):
        self.stack_items = []

    def append(self, stack_item):
        self.stack_items.append(stack_item)
        return self

    def __repr__(self):
        stack_dump = ''
        for item in self.stack_items:
            stack_dump += str(item)
        return stack_dump

    def __str__(self):
        stack_dump = ''
        for item in self.stack_items:
            stack_dump += str(item)
        return stack_dump


class StackItem:
    def __init__(self, reason, expected, actual):
        self.reason = reason
        self.expected = expected
        self.actual = actual

    def __repr__(self):
        return 'Reason: {0}\nExpected:\n{1}\nActual:\n{2}' \
               .format(self.reason, _format_value(self.expected), _format_value(self.actual))

    def __str__(self):
        return '\n\nReason: {0}\nExpected:\n{1}\nActual:\n{2}' \
               .format(self.reason, _format_value(self.expected), _format_value(self.actual))


def _indent(s):
    return '\n'.join('  ' + line for line in s.splitlines())


def _format_value(value):
    return _indent(_generate_pprint_json(value))


def _generate_pprint_json(value):
    return json.dumps(value, sort_keys=True, indent=4)


def _is_dict_same(a, b, ignore_value_of_keys):
    for key in a:
        if not key in b:
            return False, \
                   Stack().append(
                        StackItem('Expected key "{0}" Missing from Actual'
                                      .format(key),
                                  a,
                                  b))
        if not key in ignore_value_of_keys:
            are_same_flag, stack = _are_same(a[key], b[key], ignore_value_of_keys)
            if not are_same_flag:
                return False, \
                       stack.append(StackItem('Different values', a[key], b[key]))
    return True, Stack()


def _is_list_same(a, b, ignore_value_of_keys):
    for i in xrange(len(a)):
        are_same_flag, stack = _are_same(a[i], b[i], ignore_value_of_keys)
        if not are_same_flag:
            return False, \
                   stack.append(
                       StackItem('Different values (Check order)', a[i], b[i]))
    return True, Stack()

def _bottom_up_sort(unsorted_json):
    if isinstance(unsorted_json, list):
        new_list = []
        for i in xrange(len(unsorted_json)):
            new_list.append(_bottom_up_sort(unsorted_json[i]))
        return sorted(new_list)

    elif isinstance(unsorted_json, dict):
        new_dict = {}
        for key in sorted(unsorted_json):
            new_dict[key] = _bottom_up_sort(unsorted_json[key])
        return new_dict

    else:
        return unsorted_json

def _are_same(a, b, ignore_value_of_keys):
    # Check for None
    if a is None:
        return a == b, Stack()

    # Ensure they are of same type
    if type(a) != type(b):
        return False, \
               Stack().append(
                   StackItem('Type Mismatch: Expected Type: {0}, Actual Type: {1}'
                                .format(type(a), type(b)),
                             a,
                             b))

    # Compare primitive types immediately
    if type(a) in (int, str, bool, long, float, unicode):
        return a == b, Stack()

    # Ensure collections have the same length
    if len(a) != len(b):
        return False, \
               Stack().append(
                    StackItem('Length Mismatch: Expected Length: {0}, Actual Length: {1}'
                                  .format(len(a), len(b)),
                              a,
                              b))

    if isinstance(a, dict):
        return _is_dict_same(a, b, ignore_value_of_keys)

    if isinstance(a, list):
        return _is_list_same(a, b, ignore_value_of_keys)

    return False, Stack().append(StackItem('Unhandled Type: {0}'.format(type(a)), a, b))

def are_same(original_a, original_b, ignore_list_order_recursively=False, ignore_value_of_keys=[]):
    a = None
    b = None
    if ignore_list_order_recursively:
        a = _bottom_up_sort(original_a)
        b = _bottom_up_sort(original_b)
    else:
        a = original_a
        b = original_b
    return _are_same(a, b, ignore_value_of_keys)

def json_are_same(a, b, ignore_list_order_recursively=False, ignore_value_of_keys=[]):
    return are_same(json.loads(a), json.loads(b), ignore_list_order_recursively, ignore_value_of_keys)
