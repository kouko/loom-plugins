"""Test-only confined Markdown saver. Mechanical observations are not research verdicts."""
import hashlib
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import unquote, urlsplit

LIMIT = 32 * 1024
LINK_SCOPE = ('limited inline Markdown destinations outside fenced/inline code; '
              'images/reference syntax, anchors and external contents are not validated')


class SaveError(Exception):
    def __init__(self, message, *, written=False):
        super().__init__(message)
        self.written = written


def digest(data):
    return hashlib.sha256(data).hexdigest()


class SaveTool:
    def __init__(self, policy):
        self.root = Path(policy['root']).resolve(strict=True)
        if not self.root.is_dir():
            raise SaveError('root must be a directory')
        self.mode = policy.get('result_mode', 'full')
        if self.mode not in ('full', 'confirmation'):
            raise SaveError('unknown result mode')
        self.create_roots = [self._target(p) for p in policy.get('create_roots', [])]
        self.create_files = {self._target(p) for p in policy.get('create_files', [])}
        self.owned = {}
        for name in policy.get('update_files', []):
            target = self._target(name)
            if not target.is_file():
                raise SaveError('authorized update must name an existing file')
            self.owned[target] = digest(target.read_bytes())

    def _target(self, name):
        if not isinstance(name, str) or not name or '\x00' in name:
            raise SaveError('invalid path')
        path = Path(name)
        if '..' in path.parts:
            raise SaveError('write traversal is not allowed')
        path = path if path.is_absolute() else self.root / path
        if not path.is_relative_to(self.root) or path == self.root:
            raise SaveError('outside authorized root')
        relative = path.relative_to(self.root)
        if (relative.parts[0] not in ('docs', 'scratch', 'fixtureVault')
                or any(p in ('.git', '.claude', '.agents', '.codex') for p in relative.parts)
                or relative.name in ('CLAUDE.md', 'CLAUDE.local.md', 'AGENTS.md')):
            raise SaveError('protected path')
        current = self.root
        for part in relative.parts:
            current /= part
            if current.is_symlink():
                raise SaveError('symlink write path is not allowed')
        return path

    def _authorize(self, path):
        if path.suffix != '.md':
            raise SaveError('only Markdown record writes are allowed')
        if path in self.owned:
            if not path.is_file() or digest(path.read_bytes()) != self.owned[path]:
                raise SaveError('stale authorized file; external change preserved')
        elif path.exists():
            raise SaveError('collision: existing file is not authorized for overwrite')
        elif path not in self.create_files and not any(path.is_relative_to(p) and path != p for p in self.create_roots):
            raise SaveError('write not authorized by instance policy')

    def save_record(self, path, content):
        if not isinstance(content, str):
            raise SaveError('content must be text')
        data = content.encode('utf-8')
        if len(data) > LIMIT:
            raise SaveError('size exceeds complete-result cap; nothing written')
        target = self._target(path)
        self._authorize(target)
        written = False
        temporary = None
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            self._target(str(target))
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.save-probe-', delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            # Recheck the point-in-time policy before committing the prepared file.
            self._target(str(target))
            self._authorize(target)
            if target in self.owned:
                os.replace(temporary, target)
                temporary = None
            else:
                # Atomic create-if-absent; a collision cannot silently become overwrite.
                os.link(temporary, target)
            written = True
            actual = target.read_bytes()
            if actual != data:
                raise SaveError('saved bytes changed before readback', written=True)
            self.owned[target] = digest(actual)
            result = {'written': True, 'path': target.relative_to(self.root).as_posix()}
            full = dict(result, sha256=digest(actual), persisted_content=actual.decode('utf-8'),
                        readback_complete=True, observation_scope='point-in-time persisted bytes; no semantic correctness verdict',
                        **self._links(actual.decode('utf-8'), target.parent))
            return full if self.mode == 'full' else result
        except SaveError:
            raise
        except OSError as exc:
            raise SaveError('save/readback IO failed: ' + str(exc), written=written) from exc
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def _links(self, body, parent):
        lines, fence = [], None
        for line in body.splitlines():
            marker = re.match(r'^\s*(`{3,}|~{3,})', line)
            if marker:
                if fence is None:
                    fence = marker.group(1)[0]
                elif marker.group(1)[0] == fence:
                    fence = None
                continue
            if fence is None:
                lines.append(re.sub(r'`[^`]*`', '', line))
        visible = '\n'.join(lines)
        links = []
        # Deliberately narrow syntax: the fixture uses ordinary inline links.
        for match in re.finditer(r'(?<!!)\[[^\]\n]+\]\((<[^>\n]+>|[^\s)]+)(?:\s+"[^"\n]*")?\)', visible):
            raw = match.group(1).strip('<>')
            item = {'destination': raw}
            try:
                parsed = urlsplit(raw)
            except ValueError:
                item['status'] = 'malformed-unchecked'
                links.append(item)
                continue
            if raw.startswith('#') or raw == '':
                item['status'] = 'anchor-unchecked'
            elif parsed.scheme or parsed.netloc:
                item['status'] = 'external-unchecked'
            else:
                decoded = unquote(parsed.path)
                destination = Path(os.path.abspath(parent / decoded))
                if not destination.is_relative_to(self.root):
                    item['status'] = 'outside-unchecked'
                else:
                    current, symlink = self.root, False
                    for component in destination.relative_to(self.root).parts:
                        current /= component
                        if current.is_symlink():
                            symlink = True
                            break
                    item['status'] = 'symlink-unchecked' if symlink else ('exists' if destination.exists() else 'missing')
                    item['resolved_path'] = destination.relative_to(self.root).as_posix()
            links.append(item)
        return {'links': links, 'link_scope': LINK_SCOPE,
                'unsupported_reference_links': bool(re.search(r'\[[^\]\n]+\]\[[^\]\n]*\]|^\s*\[[^\]\n]+\]:', visible, re.M))}
