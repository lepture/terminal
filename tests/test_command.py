from terminal import Command


class TestCommand(object):

    def test_parse(self):
        program = Command('foo')
        program.option('-f', 'force')
        program.option('-v, --verbose', 'show more log')
        program.option('--no-color', 'output without color')
        program.option('-t, --tag <tag>', 'tag name')
        program.option('-s [source]', 'source repo')
        program.option('--key <keyword>', 'keywords')

        program.parse(
            'foo -f -v --verbose --no-color bar -t tag --key=what'
        )

        assert program.get('-f')
        assert program.verbose
        assert program.tag == 'tag'
        assert program.color is False
        assert program.key == 'what'

    def test_action(self):
        program = Command('foo')

        @program.action
        def lepture(bar):
            assert bar == 'lepture'

        program.parse('foo lepture --bar lepture')
        program.parse('foo lepture --bar lepture baz')

        assert 'baz' in program.args

        # subcommand itself
        program.action(program)
        program.parse('foo foo lepture --bar lepture')
