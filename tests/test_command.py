from terminal import Command, Option
from nose.tools import raises


class TestOption(object):

    def test_attr(self):
        o = Option('-f')
        assert repr(o) == '<Option "-f">'

    @raises(ValueError)
    def test_raise(self):
        Option('invalid name')

    def test_shortname(self):
        # shortname
        o = Option('-f')
        assert o.key == '-f'
        assert o.boolean
        assert o.default is False
        assert o.required is False

    def test_longname(self):
        o = Option('--force')

        assert o.key == 'force'
        assert o.boolean
        assert o.default is False
        assert o.required is False

        o = Option('--no-color')
        assert o.key == 'color'
        assert o.boolean
        assert o.default is True
        assert o.required is False

    def test_both_name(self):
        o = Option('-f, --force')
        assert o.key == 'force'
        assert o.boolean
        assert o.default is False
        assert o.required is False

    def test_non_boolean(self):
        o = Option('-o, --output [dir]')
        assert o.key == 'output'
        assert o.boolean is False
        assert o.default is None
        assert o.required is False

        o = Option('-o, --output <dir>')
        assert o.required is True

    def test_default(self):
        o = Option('-o, --output <dir>', 'output directory, default: src')
        assert o.default == 'src'

        o = Option('-o, --output <dir>', 'directory default: [src]')
        assert o.default == 'src'

        o = Option('-o, --output <dir>', 'directory default: <src>')
        assert o.default == 'src'

        o = Option('-o, --output <dir>', 'default: <src>, output')
        assert o.default is None

    def test_to_python(self):
        o = Option('-o, --output [dir]', 'output directory, default: src')
        assert o.to_python() == 'src'
        assert o.to_python('foo') == 'foo'

        o = Option(
            '-n, --number [int]',
            'output directory, default: 1',
            resolve=int,
        )
        assert o.to_python('12') == 12


class TestCommand(object):

    def test_parse(self):
        program = Command('foo', version='1.0.0')
        program.option('-f', 'force')
        program.option('-v, --verbose', 'show more log')
        program.option('--no-color', 'output without color')
        program.option('-t, --tag <tag>', 'tag name')
        program.option('-s [source]', 'source repo')
        program.option('--key <keyword>', 'keywords')

        program.print_version()
        program.print_help()

        program.parse(
            'foo -f -v --verbose --no-color bar -t tag --key=what'
        )

        assert program.get('-f')
        assert program.verbose
        assert program.tag == 'tag'
        assert program.color is False
        assert program.key == 'what'

    def test_print(self):
        program = Command('foo', title='foobar', version='1.0.0')
        program.print_version()
        program.print_help()

        program._usage = 'foo [options]'
        program.print_help()

    def test_action(self):
        program = Command('foo')

        @program.action
        def lepture(bar, color=True, force=False, msg='hello'):
            """
            description of lepture subcommand.

            :param bar: description of bar
            """
            assert bar == 'lepture'

        program.print_version()
        program.print_help()

        program.parse('foo lepture --bar lepture')
        program.parse('foo lepture --bar lepture baz')

        assert 'baz' in program.args

        # subcommand itself
        program.action(program)
        program.parse('foo foo lepture --bar lepture')

    def test_call(self):
        # for __call__
        program = Command('foo')

        @program
        def bar():
            return 'bar'

        program.print_help()

    @raises(RuntimeError)
    def test_missing_option(self):
        program = Command('foo')
        program.option('-o, --output <dir>', 'output directory')
        program.parse('foo -o')

    @raises(RuntimeError)
    def test_missing_required(self):
        program = Command('foo')
        program.option('-o, --output <dir>', 'output directory')
        program.parse('foo')

    @raises(AttributeError)
    def test_attr(self):
        program = Command('foo')
        program.bar

    @raises(ValueError)
    def test_get(self):
        program = Command('foo')
        program.get('bar')

    def test_get_default(self):
        program = Command('foo')
        program.option('--output [dir]', 'output dir, default: site')
        assert program.output == 'site'

    def test_run_parse(self):
        program = Command('foo')

        def func(**kwargs):
            print('func')

        program._command_func = func
        program.parse()
