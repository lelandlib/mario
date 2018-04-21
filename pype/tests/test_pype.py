
import pytest
from click.testing import CliRunner
from hypothesis import given
from hypothesis.strategies import text
import toolz

import pype
import pype.app


@pytest.mark.parametrize(
    'args,  expected',
    [
        (['str.replace(?, ".", "!")', '?', ('a.b.c\n',)], 'a!b!c\n'),
        (['-p$', 'str.replace($, ".", "!")', '$', ('a.b.c\n',)], 'a!b!c\n'),
        (
            [
                '-icollections',
                '-ijson',
                'json.dumps(dict(collections.Counter(str.replace(?, ".", "!"))))',
                '?',
                ('a.b.c',)
            ],
            '{"a": 1, "!": 2, "b": 1, "c": 1}'
        ),
        (
            [
                '-icollections',
                '-ijson',
                'str.replace(?, ".", "!") '
                '|| collections.Counter(?) '
                '|| dict(?) '
                '|| json.dumps(?) ',
                '?',
                ('a.b.c',)
            ],
            '{"a": 1, "!": 2, "b": 1, "c": 1}'
        ),
        (
            [
                '-icollections',
                '-ijson',
                'str.replace(?, ".", "!") '
                '|| collections.Counter '
                '|| dict '
                '|| json.dumps ',
                '?',
                ('a.b.c',)
            ],
            '{"a": 1, "!": 2, "b": 1, "c": 1}'
        ),
        (
            [
                "-i", "toolz",
                "-i", "collections",
                ' str.replace(?, ".", "!") || collections.Counter',
                'toolz.merge_with(sum, ?)',
                ("a.b.c\n", "d.e.f\n",),
            ],
            r"{'a': 1, '!': 4, 'b': 1, 'c': 1, '\n': 2, 'd': 1, 'e': 1, 'f': 1}"
        )
    ],
)
def test_cli(args, expected):

    runner = CliRunner()
    result = runner.invoke(pype.app.cli, args)
    assert not result.exception
    assert result.output.strip() == expected.strip()


@pytest.mark.parametrize(
    'command, expected',
    [
        ('str.upper(?)', ['str.upper(value)']),
        ('str.upper', ['str.upper(value)']),
        ('str.upper(?) || "X".join', ['str.upper(value)', '"X".join(value)']),
    ]
)
def test_make_pipeline(command, expected):
    assert pype.app.make_pipeline_strings(command, '?') == expected


@pytest.mark.skip
def test_newlines():
    input_string = """

    """

    runner = CliRunner()
    result = runner.invoke(pype.app.cli, args)
    assert result.output == expected