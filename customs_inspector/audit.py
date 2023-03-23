import difflib
import glob
import os
import shutil
import re
import secrets
import signal
import webbrowser
from pathlib import Path
from threading import Thread
from zipfile import ZipFile

import bottle
from bottle import Bottle, request, static_file

from customs_inspector.server import Server

diff_path = None
pkg_name = ''
old_pkg_version = ''
new_pkg_version = ''
result = False

diff = {
    'ADDED': [],
    'REMOVED': [],
    'DIFF': [],
    'NO_DIFF': [],
}
diff_human_names = {
    'ADDED': 'Files Added',
    'REMOVED': 'Files Removed',
    'DIFF': 'Files Changed',
    'NO_DIFF': 'Files Unchanged',
}

static_folder = '/'.join(__file__.split('/')[:-1]) + '/static'
header = Path(f'{static_folder}/header.template').read_text()
footer = Path(f'{static_folder}/footer.template').read_text()
stop = Path(f'{static_folder}/stop.template').read_text()


def get_old_pkg_files(package_name: str, env):
    '''
    Runs pip show and extract the location of the old package
    '''
    output = env.run_pip("show", package_name)
    path = (
        re.search('Location: (.*)\n', output).group(0).split(' ')[1].replace("\n", "")
    )
    full_path = f'{path}/{package_name}'
    if os.path.isdir(full_path):
        files = [
            file.replace(f'{full_path}/', '')
            for file in glob.glob(f'{full_path}/**/*.py', recursive=True)
        ]
        return files, full_path


def open_silently(path: str):
    try:
        return open(path, 'r')
    except FileNotFoundError:
        pass


def generate_duplicates(old_lines, new_lines, filename):
    old_path = Path(f'{diff_path}/{filename}.old')
    new_path = Path(f'{diff_path}/{filename}.new')
    old_path.parent.mkdir(exist_ok=True, parents=True)
    old_path.write_text(old_lines)
    new_path.write_text(new_lines)

def get_new_pkg_files(archive, pkg_name):
    path = f'/tmp/{secrets.token_hex(24)}'
    ZipFile(archive).extractall(path)
    new_files = [
        file.replace(f'{path}/{pkg_name}/', '')
        for file in glob.glob(
            f'{path}/{pkg_name}/**/*.py',
            recursive=True,
        )
    ]
    return new_files, path

def audit(old_pkg, archive, new_version, env):
    global diff
    global diff_path
    global pkg_name
    global old_pkg_version
    global new_pkg_version
    pkg_name = old_pkg.complete_name
    old_pkg_version = old_pkg.version
    new_pkg_version = new_version
    old_files, old_files_path = get_old_pkg_files(pkg_name, env)
    new_files, new_files_path = get_new_pkg_files(archive, pkg_name) 
    combined_files = set(new_files + old_files)
    diff_path = f'/tmp/{secrets.token_hex(24)}'
    for file in combined_files:
        new = open_silently(f'{new_files_path}/{pkg_name}/{file}')
        old = open_silently(f'{old_files_path}/{file}')
        if not new:
            generate_duplicates(old.read(), '', file)
            diff['REMOVED'].append(file)
        elif not old:
            generate_duplicates('', new.read(), file)
            diff['ADDED'].append(file)
        else:
            if (
                difflib.SequenceMatcher(
                    None, old.read(), new.read()
                ).real_quick_ratio()
                == 1.0
            ):
                old.seek(0)
                content = old.read()
                generate_duplicates(content, content, file)
                diff['NO_DIFF'].append(file)
            else:
                old.seek(0)
                new.seek(0)
                generate_duplicates(old.read(), new.read(), file)
                diff['DIFF'].append(file)
        if new:
            new.close()
        if old:
            old.close()
    print(f'Please audit {pkg_name} before updating')
    webbrowser.open('http://localhost:7040')
    app.run(server=server)
    shutil.rmtree(diff_path)
    if not result:
        raise Exception(
            f'{pkg_name} failed your audit! Please report it as a malicious package.'
        )

app = Bottle()
server = Server(port=7040)

@app.route('/')
def index():
    body = ''
    for diff_type, files in diff.items():
        # TODO: escape HTML
        body += '<details>'
        body += f'<summary>{diff_human_names[diff_type]} ({len(files)})</summary>'
        files.sort()
        for file in files:
            body += f'<div style="display:flex;"><input type="checkbox" /><a href="/file/?file={file}" target="_blank">{file}</a></div>'
        body += '</details>'
    return header.format(pkg_name, old_pkg_version, new_pkg_version) + body + footer


@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=static_folder)


@app.route('/file/')
def server_get_file():
    return Path(f'{static_folder}/diff.html').read_text()


@app.route('/raw/')
def raw():
    # TODO: does this suffieciently handle directory traversal?
    filename = request.query.file
    if not filename.endswith('.old') and not filename.endswith('.new') or '../' in filename:
        print(filename)
        raise Exception('Cannot read non Python files.')
    path = Path(f'{diff_path}/{filename}')
    return path.read_text()


@app.route('/stop/')
def stopserver():
    global result
    if request.query.result == "confirm":
        result = True
    else:
        result = False
    thread = Thread(target=server.stop).start()
    return header.format(pkg_name, old_pkg_version, new_pkg_version) + stop
