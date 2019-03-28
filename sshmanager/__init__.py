from __future__ import unicode_literals
import xml.etree.ElementTree as ET
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion import WordCompleter
from fuzzyfinder import fuzzyfinder
from prompt_toolkit import PromptSession
import subprocess
from pathlib import Path

home = str(Path.home())

root = ET.parse(home + '/.sshman/servertree.xml').getroot()

serverdictionary = {}
serverlist = []


class SSHCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, serverlist)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


def recursive(node):
    for expanding_node in node.findall('./Node'):
        displaytext = expanding_node.find('./DisplayName').text
        if (expanding_node.get('Type') == "1"):
            serverlist.append(displaytext)
            serverdictionary[displaytext] = {
                'ServerName': expanding_node.find('./ServerName').text,
                'CLParams': expanding_node.find('./CLParams').text,
                'UserName': expanding_node.find('./UserName').text,
            }

        expanded = expanding_node.get('Expanded')
        if (expanded):
            recursive(expanding_node)


def find(node):
    command = 'ssh ' + serverdictionary[node].get('UserName') + '@' + serverdictionary[node].get('CLParams')
    subprocess.call(command, shell=True)


def main():
    print('parsing xml...')
    putty = root.find('./Putty')
    recursive(putty)
    print("Printing serverlist:")
    for item in serverdictionary:
        print(item)
    print('\n' + 'done!')
    session = PromptSession(completer=WordCompleter(serverlist))

    while True:
        try:
            text = session.prompt('ssh inzicht@')
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        else:
            if (text == ''):
                continue
            find(text)
    print('GoodBye!')


if __name__ == '__main__':
    main()


