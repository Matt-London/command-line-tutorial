from ..filesystem.Directory import Directory
from ..resources import variables as var


class Interpreter:

    _default_command_mapping = {
        "ls":  lambda instance, *args: instance.get_directory().ls(),
        "pwd": lambda instance, *args: print(instance.get_directory().name)
    }

    def __init__(self, directory=None, commands=None):
        self._history = []

        if not directory:
            directory = Directory("/")

        self._command_mapping = {}

        if not commands:
            commands = self._default_command_mapping

        for name, cmd in commands.items():
            if not self.add_command(name, cmd):
                raise ValueError("unable to add command %s (%s) - somehow conflicts with another command" % (name, cmd))

        self._directory = directory
        self._return = 0
        self._cmd = []

    def get_directory(self):
        return self._directory

    def get_history(self):
        return list(self._history)

    def get_return_code(self):
        return self._return

    def get_commands(self):
        return set(self._command_mapping)

    def add_command(self, name, command, force=False):
        try:
            is_func = callable(command)
        except (UnboundLocalError, TypeError):
            globals()["callable"] = lambda obj: hasattr(obj, '__call__')
            is_func = callable(command)

        if not is_func:
            raise ValueError("provided command '%s' (value: %s) is not a function" % (name, command))

        if force or not (name in self._command_mapping):
            self._command_mapping[name] = command
            return True

        return False

    def remove_command(self, name):
        if name in self._command_mapping:
            self._command_mapping.pop(name)
            return True

        return False

    def interpret(self, line):
        if not line:
            return

        self._cmd.append(line)
        cmd_str = "\n".join(self._cmd)
        if not self._check_quotes(cmd_str):
            return False

        command = []

        quote = ""
        tmp = ""

        # If you have a better way to do this, please let me know
        for i in cmd_str:
            if i == " " and not quote:
                if not tmp:
                    continue

                command.append(tmp)
                tmp = ""
            elif i == quote:
                command.append(tmp)
                quote = ""
                tmp = ""
            elif not quote and (i == '"' or i == "'"):
                quote = i
            else:
                tmp += i

        if tmp:
            command.append(tmp)

        self._history.append(cmd_str)
        self._cmd = []

        # print("Executing " + str(command))

        try:
            self._return = self._evaluate(command[0], *command[1:])
        except Exception as e:
            print(e)
            self._return = -1

        if self._return < 0:
            print(var.shell + ": '%s': command not found..." % command[0].replace("\n", "\\n"))
            self._return = 127

        return True

    def _evaluate(self, command, *args):

        if not (command in self._command_mapping):
            return -1

        cmd = self._command_mapping[command]
        ret = cmd(self, *args)

        if not (type(ret) is int) and not (ret is None):
            raise ValueError("return type must be int or None, not " + str(type(ret)))

        ret = 0 if ret is None else ret

        if ret < 0:
            ret = 127 + (ret % 127)

        if ret > 127:
            ret %= 127

        return ret

    @staticmethod
    def _check_quotes(line):
        quote = ""

        for i in line:
            if i == quote:
                quote = ""
            elif not quote and (i == '"' or i == "'"):
                quote = i

        return quote == ""
