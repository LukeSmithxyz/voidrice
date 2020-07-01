"""This module defines data parser
which can be used to exchange information between processes.
"""
import json
import abc
import shlex
import itertools
import enum


class Parser:
    """Subclasses of this abstract class define
    how to input will be parsed.
    """

    @staticmethod
    @abc.abstractmethod
    def get_name():
        """Returns the constant name which is associated to this parser."""
        raise NotImplementedError()

    @abc.abstractmethod
    def parse(self, line):
        """Parses a line.

        Args:
            line (str): read line

        Returns:
            dict containing the key value pairs of the line
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def unparse(self, data):
        """Composes the data to a string
        whichs follows the syntax of the parser.

        Args:
            data (dict): data as key value pairs

        Returns:
            string
        """
        raise NotImplementedError()


class JsonParser(Parser):
    """Parses json input"""

    @staticmethod
    def get_name():
        return 'json'

    def parse(self, line):
        try:
            data = json.loads(line)
            if not isinstance(data, dict):
                raise ValueError(
                    'Expected to parse an json object, got ' + line)
            return data
        except json.JSONDecodeError as error:
            raise ValueError(error)

    def unparse(self, data):
        return json.dumps(data)


class SimpleParser(Parser):
    """Parses key value pairs separated by a tab.
    Does not support escaping spaces.
    """
    SEPARATOR = '\t'

    @staticmethod
    def get_name():
        return 'simple'

    def parse(self, line):
        components = line.split(SimpleParser.SEPARATOR)

        if len(components) % 2 != 0:
            raise ValueError(
                'Expected key value pairs, ' +
                'but at least one key has no value: ' +
                line)

        return {
            key: value
            for key, value in itertools.zip_longest(
                components[::2], components[1::2])
        }

    def unparse(self, data):
        return SimpleParser.SEPARATOR.join(
            str(key) + SimpleParser.SEPARATOR + str(value.replace('\n', ''))
            for key, value in data.items())


class BashParser(Parser):
    """Parses input generated
    by dumping associative arrays with `declare -p`.
    """

    @staticmethod
    def get_name():
        return 'bash'

    def parse(self, line):
        # remove 'typeset -A varname=( ' and ')'
        start = line.find('(')
        end = line.rfind(')')

        if not 0 <= start < end:
            raise ValueError(
                "Expected input to be formatted like "
                "the output of bashs `declare -p` function. "
                "Got: " + line)

        components = itertools.dropwhile(
            lambda text: not text or text[0] != '[',
            shlex.split(line[start + 1:end]))
        return {
            key[1:-1]: value
            for pair in components
            for key, value in (pair.split('=', maxsplit=1),)
        }

    def unparse(self, data):
        return ' '.join(
            '[' + str(key) + ']=' + shlex.quote(value)
            for key, value in data.items())


@enum.unique
class ParserOption(str, enum.Enum):
    JSON = JsonParser
    SIMPLE = SimpleParser
    BASH = BashParser

    def __new__(cls, parser_class):
        inst = str.__new__(cls)
        inst._value_ = parser_class.get_name()
        inst.parser_class = parser_class
        return inst
