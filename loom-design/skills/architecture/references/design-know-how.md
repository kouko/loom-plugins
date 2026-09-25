# Design know-how

The heuristics the architecture tool draws on when it proposes options.
Each is a starting point to put in front of the user as an option with a
trade-off, never a verdict. Tool versions drift: re-check a number against
its source before quoting it as current.

## Module split and dependency direction

- **Dependencies point inward, toward policy, never toward details.**
  Nothing in an inner layer knows anything about an outer one; the number
  of layers is not fixed, so propose the rule, not a fixed folder set.
  <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
- **Ports and adapters** is the same rule as inside/outside: the core knows
  ports, each external device gets an adapter. Offer it when the project
  has more than one real driver (UI, CLI, tests) or a swappable backend.
  <https://alistair.cockburn.us/hexagonal-architecture/>
- **Dependency inversion keeps the rule when control flows outward**: the
  high-level module owns the interface, the low-level one implements it.
  <https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles>
- **No cycles between top-level modules is the first checkable rule.**
  Cycles are what killed modularity at Shopify, removed with dependency
  inversion and publish/subscribe.
  <https://shopify.engineering/shopify-monolith>
- **Recommended first rules**: (1) no cycles between top-level modules;
  (2) the core imports no adapter, UI or infrastructure module; (3) only the
  composition root (app entry, `cmd/`) imports everything.
- **Layer-first for a small project; split by domain when a layer grows.**
  Presentation-domain-data layering suits small granularity; once a layer
  gets too big, split the top level into domain modules, each internally
  layered. <https://martinfowler.com/bliki/PresentationDomainDataLayering.html>
- **Top-level names say what the system does**, not which framework it
  uses — a review check for any proposed tree.
  <https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html>
- **Split where the language changes**: the same word meaning different
  things in two areas marks a boundary.
  <https://martinfowler.com/bliki/BoundedContext.html>
- **Extract on the third occurrence, not the second** (the rule of three).
  A second consumer is a reason to consider extraction, not a trigger.
  <https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)>
  A wrong abstraction costs more than duplication; when one is wrong,
  re-inline it. <https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction>
- **No structure for presumptive features** (YAGNI); it has a cost of
  carry. <https://martinfowler.com/bliki/Yagni.html>
- **Modular monolith first.** Most successful service architectures started
  as a monolith that grew too big; boundaries are hard to get right up
  front. <https://martinfowler.com/bliki/MonolithFirst.html>
  Services buy strong boundaries, independent deploy and technology
  diversity, and cost distribution, eventual consistency and operations;
  a small team gets the boundaries in-process with enforced module rules.
  <https://martinfowler.com/articles/microservice-trade-offs.html>
  Extract a service only for a named reason.
  <https://shopify.engineering/shopify-monolith>

## Folder structure per ecosystem

- **Python**: an installable project or library → `src/<pkg>/` + `tests/`;
  a single-file script → flat is acceptable. src layout prevents importing
  the in-development copy by accident, at the cost of needing an install to
  run. <https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/>
  pytest strongly suggests src layout and tests outside the application
  code for new projects.
  <https://docs.pytest.org/en/stable/explanation/goodpractices.html>
- **Swift**: SwiftPM targets live under `Sources/<Target>/`, tests under
  `Tests/<Target>/`.
  <https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html>
  Modularize an Xcode app with local packages; networking and utilities
  are good first candidates.
  <https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages>
  A target is a compile-time boundary: `internal` is the default access
  level, and `package` (SE-0386) shares symbols within a package only.
  <https://github.com/swiftlang/swift-evolution/blob/main/proposals/0386-package-access-modifier.md>
- **Go**: start at the smallest layout — one package or command at the
  module root; supporting packages under `internal/`; several commands
  under `cmd/`. <https://go.dev/doc/modules/layout>
  `internal/` is compiler-enforced.
  <https://pkg.go.dev/cmd/go#hdr-Internal_Directories>
  `golang-standards/project-layout` is not an official standard.
  <https://github.com/golang-standards/project-layout/issues/117>
  `_test.go` files sit beside the code.
- **TypeScript / Node**: a monorepo is one root package with workspaces
  (<https://docs.npmjs.com/cli/v10/using-npm/workspaces>,
  <https://pnpm.io/workspaces>); project references make the compiler
  respect package boundaries.
  <https://www.typescriptlang.org/docs/handbook/project-references.html>
- **Entry points apart from logic** (`cmd/` in Go, adapters driving the
  core). <https://go.dev/doc/modules/layout>

### File size defaults

Tool defaults, a starting ceiling the user may change:

| Tool | Rule | Default |
|---|---|---|
| SwiftLint | `file_length` | warning 400, error 1000 lines — <https://realm.github.io/SwiftLint/file_length.html> |
| ESLint | `max-lines` | 300 lines — <https://eslint.org/docs/latest/rules/max-lines> |
| Pylint | `too-many-lines` | 1000 lines — <https://pylint.readthedocs.io/en/stable/user_guide/messages/convention/too-many-lines.html> |

## Main technology choices

Compare options on these dimensions:

- **Maturity**: boring technology has known failure modes; new technology
  has unknown ones. <https://mcfunley.com/choose-boring-technology>
- **Innovation tokens**: a team gets about three; count how many new
  technologies an option spends. Ask how the problem would be solved
  without adding anything new. Same source.
- **Operational cost**: every added technology must be monitored, tested
  and learned; keeping a system running costs more than building it. Same
  source.
- **Reversibility**: a framework is sticky and hard to reverse, a library
  is swappable; decide frameworks with more care.
  <https://qiita.com/hirokidaichi/items/a746062917595619720b>
- **Maturity vocabulary**: Adopt, Trial, Assess, Caution.
  <https://www.thoughtworks.com/radar/faq>

Present options in MADR's shape: drivers, considered options, the outcome,
and per option "good, because … / bad, because …".
<https://github.com/adr/madr/blob/develop/template/adr-template.md>

## CI stages

- **Baseline order** (a synthesis of the sources below, not one source's
  list): (1) lint + tests + build or type-check on every change → (2) the
  architecture-rule guards as ordinary tests → (3) dependency updates and
  security scanning → (4) release automation.
  <https://martinfowler.com/articles/continuousIntegration.html>,
  <https://docs.github.com/en/actions/tutorials/build-and-test-code/python>,
  <https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates>
- Security scanning is free on public repositories and paid on private
  ones. <https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security>
- **macOS runners cost about ten times Linux** per minute on GitHub-hosted
  runners (<https://docs.github.com/en/billing/reference/actions-runner-pricing>);
  for a private Xcode project, test pure-logic packages on Linux where they
  compile and keep macOS jobs for the app target. Xcode Cloud includes
  compute hours with Apple Developer Program membership.
  <https://developer.apple.com/xcode-cloud/>

## Encoding rules as guards

| Ecosystem | Tool |
|---|---|
| Python | import-linter contracts (layers, forbidden, independence, acyclic) — <https://import-linter.readthedocs.io/en/stable/> |
| JS / TS | dependency-cruiser rules (no-circular, forbidden) — <https://github.com/sverweij/dependency-cruiser>; project references |
| JVM | ArchUnit layer and cycle rules — <https://www.archunit.org/userguide/html/000_Index.html> |
| Go | `internal/`; depguard and gomodguard via golangci-lint — <https://golangci-lint.run/docs/linters/configuration/> |
| Swift | SwiftPM targets and access control; SwiftLint `custom_rules` — <https://github.com/realm/SwiftLint/blob/main/README.md> |

`go vet` is not a boundary tool. <https://pkg.go.dev/cmd/vet>
