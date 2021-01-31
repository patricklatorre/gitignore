import requests
import json
import sys


def get_masterlist():
    # Fetch @github/gitignore repo data
    master_url = 'https://api.github.com/repos/github/gitignore/commits/master'
    sha = json.loads(requests.get(master_url).text)['sha']

    tree_url = f'https://api.github.com/repos/github/gitignore/git/trees/{sha}'
    tree = json.loads(requests.get(tree_url).text)['tree']

    # Get filenames excluding configs
    all_paths = map(lambda fileobj: fileobj['path'], tree)
    paths = [p for p in all_paths if p.endswith('.gitignore')]

    # Remove file ext and use lowercased name as key
    masterlist = {}
    for p in paths:
        name = p.replace('.gitignore', '')
        masterlist[name.lower()] = name

    return masterlist


def download_gitignore(name):
    url = f'https://raw.githubusercontent.com/github/gitignore/master/{name}.gitignore'
    return requests.get(url).text


print("> Getting Github's official masterlist")
masterlist = get_masterlist()

args = [arg.lower() for arg in sys.argv[1:]]
out_file = ''
successes = 0

for arg in args:
    name = masterlist.get(arg)
    if name is not None:
        content = download_gitignore(name)
        out_file = out_file + content + '\n'
        successes = successes + 1
        print('  ✔ ' + name)
    else:
        print('  ✖ ' + arg)

with open('.gitignore', 'a') as file:
    file.write(out_file)

print(f'> Successfully added {successes} starters to .gitignore')
