#!/usr/bin/env python3
"""Create and validate managed or explicitly selected diagram files."""

import importlib.util
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

BACKENDS = Path(__file__).resolve().parent.parent / "backends"
DIAGRAMS = Path("diagrams")
LABEL = r"(?:\\.|[^\\\]\n])+"
CHANGE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")


def change_args(args):
    """Extract an optional explicit change id without changing positional arguments."""
    args = list(args)
    if "--change-id" not in args:
        return args, None
    index = args.index("--change-id")
    if index + 1 >= len(args) or args.count("--change-id") != 1:
        raise ValueError("--change-id requires one id")
    change_id = args[index + 1]
    del args[index:index + 2]
    return args, change_id


def option_args(args, flag):
    args = list(args)
    if flag not in args:
        return args, None
    index = args.index(flag)
    if args.count(flag) != 1 or index + 1 >= len(args) or args[index + 1].startswith("--"):
        raise ValueError(f"{flag} requires one directory")
    value = args[index + 1]
    del args[index:index + 2]
    return args, value


def destination_args(args):
    args, change_id = change_args(args)
    args, output_dir = option_args(args, "--output-dir")
    if output_dir is not None:
        if change_id is not None:
            raise ValueError("--output-dir cannot be combined with --change-id")
        cwd = Path.cwd()
        root = next((path for path in (cwd, *cwd.parents) if (path / "docs/loom/intent").is_dir()), None)
        if root is not None:
            store = root / "docs/loom"
            relative = cwd.relative_to(store) if cwd.is_relative_to(store) else Path()
            if relative.parts and (store / "intent" / f"{relative.parts[0]}.md").is_file():
                raise ValueError("--output-dir cannot be used inside a Loom change")
        return args, Path(output_dir).absolute(), False
    try:
        return args, managed_directory(change_id), True
    except ValueError as error:
        if str(error).startswith("cannot find docs/loom/intent"):
            raise ValueError("destination required outside Loom; use --output-dir DIR") from error
        raise


def managed_directory(change_id):
    cwd = Path.cwd()
    root = next((path for path in (cwd, *cwd.parents) if (path / "docs/loom/intent").is_dir()), None)
    if root is None:
        raise ValueError("cannot find docs/loom/intent; run inside the repository")
    store = root / "docs/loom"
    if not store.resolve().is_relative_to(store):
        raise ValueError(f"{store}: managed docs/loom directory escapes repository")
    relative = cwd.relative_to(store) if cwd.is_relative_to(store) else Path()
    enclosing = relative.parts[0] if relative.parts and relative.parts[0] != "intent" else None
    if change_id is None:
        change_id = enclosing
    if not change_id:
        raise ValueError("cannot identify change; use --change-id <id> or run from its docs/loom/<id> directory")
    if not CHANGE_ID.fullmatch(change_id):
        raise ValueError(f"invalid change id: {change_id}")
    if enclosing and enclosing != change_id:
        raise ValueError(f"--change-id {change_id} mismatches enclosing change {enclosing}")
    intent = store / "intent" / f"{change_id}.md"
    if not intent.is_file():
        raise ValueError(f"missing intent: {intent}")
    change = store / change_id
    if not change.resolve().is_relative_to(change):
        raise ValueError(f"{change}: managed change directory escapes its location")
    managed = change / "diagrams"
    if managed.resolve() != managed:
        raise ValueError(f"{managed}: managed diagrams directory escapes canonical diagrams location")
    return managed


def bounded(path, managed):
    if not path.resolve().is_relative_to(managed.resolve()):
        raise ValueError(f"{path}: outside managed directory {managed}")


def backends():
    found = {}
    for path in sorted(BACKENDS.glob("*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        identifier = module.id()
        if identifier in found:
            raise ValueError(f"duplicate backend: {identifier}")
        found[identifier] = module
    return found


def projection_path(diagram):
    return diagram.with_name(f"{diagram.stem}.projection.md")


def backend_for(diagram, registry):
    projection = projection_path(diagram)
    if not projection.is_file():
        raise ValueError(f"{diagram}: missing {projection}")
    first = projection.read_text(encoding="utf-8").splitlines()
    if not first or not first[0].startswith("backend: "):
        raise ValueError(f"{projection}: missing backend header")
    identifier = first[0].removeprefix("backend: ").strip()
    if identifier not in registry:
        raise ValueError(f"{projection}: unknown backend {identifier}; registered: {', '.join(sorted(registry))}")
    backend = registry[identifier]
    if diagram.suffix != backend.extension():
        raise ValueError(f"{diagram}: expected {backend.extension()} for {identifier}")
    return backend


def backend_for_extension(diagram, registry):
    for backend in registry.values():
        if diagram.suffix == backend.extension():
            return backend
    raise ValueError(f"{diagram}: unsupported diagram extension")


def checked_source(diagram, registry):
    if diagram.resolve() != diagram.absolute():
        raise ValueError(f"{diagram}: symlinked diagram; select resolved path")
    if not diagram.is_file():
        raise ValueError(f"{diagram}: missing or invalid diagram")
    backend = backend_for_extension(diagram, registry)
    backend.check(diagram)
    return backend


def markdown_targets(text):
    """Yield inline, explicit, and shortcut reference-link destinations."""
    definitions = {
        label.casefold(): target.strip("<>")
        for label, target in re.findall(
            rf"(?m)^[ \t]{{0,3}}\[({LABEL})\]:[ \t]*(<[^>\n]+>|\S+)", text
        )
    }
    for match in re.finditer(rf"\[{LABEL}\]\(", text):
        start = match.end()
        depth = 1
        for index in range(start, len(text)):
            if text[index] == "(":
                depth += 1
            elif text[index] == ")":
                depth -= 1
                if depth == 0:
                    destination = text[start:index].strip()
                    if destination.startswith("<"):
                        destination = destination[1:destination.find(">")] if ">" in destination else ""
                    else:
                        destination = destination.split(maxsplit=1)[0] if destination else ""
                    yield destination
                    break
    for match in re.finditer(rf"\[({LABEL})\]\[({LABEL})?\]", text):
        label = (match.group(2) or match.group(1)).casefold()
        if label in definitions:
            yield definitions[label]
    for match in re.finditer(rf"\[({LABEL})\](?![\[(])", text):
        if text[match.end():].startswith(":") and not text[text.rfind("\n", 0, match.start()) + 1:match.start()].strip():
            continue
        label = match.group(1).casefold()
        if label in definitions:
            yield definitions[label]


def diagrams(registry):
    suffixes = {backend.extension() for backend in registry.values()}
    found = {path.resolve() for path in DIAGRAMS.glob("*") if path.is_file() and path.suffix in suffixes}
    spec = Path("spec.md")
    if spec.is_file():
        for target in markdown_targets(spec.read_text(encoding="utf-8")):
            linked = Path(unquote(target))
            if linked.suffix in suffixes:
                found.add((spec.parent / linked).resolve())
    return sorted(found)


def create(args, registry):
    args, directory, managed = destination_args(args)
    if len(args) == 1:
        identifier, name = "drawio", args[0]
    elif len(args) == 2:
        identifier, name = args
    else:
        raise ValueError("usage: diagram.py new [backend-id] <name>")
    if identifier not in registry:
        raise ValueError(f"unknown backend {identifier}; registered: {', '.join(sorted(registry))}")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", name):
        raise ValueError("diagram name must contain only letters, digits, _ or -")
    backend = registry[identifier]
    diagram = directory / f"{name}{backend.extension()}"
    projection = projection_path(diagram)
    if managed:
        bounded(diagram, directory)
        bounded(projection, directory)
    if diagram.exists() or projection.exists() or diagram.is_symlink() or projection.is_symlink():
        raise ValueError(f"{diagram}: already exists")
    directory.mkdir(parents=True, exist_ok=True)
    backend.generate(diagram)
    projection.write_text(backend.project(diagram) + "\n", encoding="utf-8")
    print(diagram)
    print(projection)


def copy(args, registry):
    args, directory, managed = destination_args(args)
    if len(args) != 1:
        raise ValueError("usage: diagram.py copy <source> [--change-id ID|--output-dir DIR]")
    source = Path(args[0])
    backend = checked_source(source, registry)
    diagram = directory / source.name
    projection = projection_path(diagram)
    if managed:
        bounded(diagram, directory)
        bounded(projection, directory)
    if diagram.exists() or projection.exists() or diagram.is_symlink() or projection.is_symlink():
        raise ValueError(f"{diagram}: already exists")
    directory.mkdir(parents=True, exist_ok=True)
    projection_text = backend.project(source) + "\n"
    diagram_created = False
    projection_created = False
    try:
        with source.open("rb") as input_file, diagram.open("xb") as output_file:
            diagram_created = True
            shutil.copyfileobj(input_file, output_file)
        with projection.open("x", encoding="utf-8") as output_file:
            projection_created = True
            output_file.write(projection_text)
    except (OSError, ValueError):
        if projection_created:
            projection.unlink(missing_ok=True)
        if diagram_created:
            diagram.unlink(missing_ok=True)
        raise
    print(diagram)
    print(projection)


def chosen(args, registry):
    if len(args) > 1:
        raise ValueError("expected at most one diagram path")
    if args:
        return [Path(args[0])]
    result = diagrams(registry)
    if not result:
        raise ValueError(f"{DIAGRAMS}: no diagram files")
    return result


def project(args, registry):
    args = list(args)
    if "--in-place" in args:
        if args.count("--in-place") != 1:
            raise ValueError("--in-place must appear once")
        args.remove("--in-place")
        args, change_id = change_args(args)
        if change_id is not None or len(args) != 1:
            raise ValueError("usage: diagram.py project <path> --in-place")
        diagram = Path(args[0])
        backend = checked_source(diagram, registry)
        projection = projection_path(diagram)
        if projection.is_symlink():
            raise ValueError(f"{projection}: symlinked projection; select a safe destination")
        if projection.exists():
            backend = backend_for(diagram, registry)
        projection.write_text(backend.project(diagram) + "\n", encoding="utf-8")
        print(projection)
        return
    args, change_id = change_args(args)
    managed = managed_directory(change_id)
    if len(args) > 1:
        raise ValueError("expected at most one diagram path")
    if args:
        selected = [Path(args[0])]
    else:
        suffixes = {backend.extension() for backend in registry.values()}
        selected = sorted(path for path in managed.glob("*") if path.is_file() and path.suffix in suffixes)
        if not selected:
            raise ValueError(f"{managed}: no diagram files")
    for diagram in selected:
        bounded(diagram, managed)
        bounded(projection_path(diagram), managed)
    for diagram in selected:
        backend = backend_for(diagram, registry)
        backend.check(diagram)
        projection = projection_path(diagram)
        projection.write_text(backend.project(diagram) + "\n", encoding="utf-8")
        print(projection)


def check(args, registry):
    failures = 0
    for diagram in chosen(args, registry):
        try:
            backend = backend_for(diagram, registry)
            backend.check(diagram)
            expected = backend.project(diagram).splitlines()
            actual = projection_path(diagram).read_text(encoding="utf-8").splitlines()
            if actual != expected:
                for index in range(max(len(actual), len(expected))):
                    old = actual[index] if index < len(actual) else "<missing>"
                    new = expected[index] if index < len(expected) else "<missing>"
                    if old != new:
                        raise ValueError(f"{projection_path(diagram)}: line {index + 1}: {old!r} != {new!r}")
            print(f"{diagram}: projection matches")
        except (ValueError, OSError) as error:
            print(error, file=sys.stderr)
            failures += 1
    return 1 if failures else 0


def main():
    if len(sys.argv) < 2:
        raise ValueError("usage: diagram.py <new|copy|project|check|list-backends> [...]")
    command, args = sys.argv[1], sys.argv[2:]
    registry = backends()
    if command == "list-backends":
        if args:
            raise ValueError("list-backends takes no arguments")
        print("\n".join(sorted(registry)) if registry else "(none)")
    elif command == "new":
        create(args, registry)
    elif command == "copy":
        copy(args, registry)
    elif command == "project":
        project(args, registry)
    elif command == "check":
        return check(args, registry)
    else:
        raise ValueError(f"unknown command: {command}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
