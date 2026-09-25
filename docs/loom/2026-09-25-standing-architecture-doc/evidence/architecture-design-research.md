# Architecture design research — evidence for the `architecture` skill

Gathered 2026-09-25 for loom-design `architecture` (the skill that designs a
project's engineering architecture and folder structure with the user, once
per project). Every bullet carries the source it rests on. Items marked
**(unverified)** could not be confirmed against a primary source in this pass.
Numeric defaults were checked against the tool's docs or source code on
2026-09-25; tool versions drift, so re-check before quoting a number as current.

---

## 1. Module boundaries and dependency direction

### Dependency direction

- **One rule survives every layered style: source dependencies point inward, toward policy, never toward details.** "Source code dependencies can only point inwards. Nothing in an inner circle can know anything at all about something in an outer circle." The number of rings is not fixed ("There's no rule that says you must always have just these four"). Propose the *rule*, not a fixed four-ring folder set. — https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- **Hexagonal (ports and adapters) is the same rule stated as inside/outside.** Intent: "Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases." Each external device gets an adapter; the core only knows ports. Use it when the project has more than one real driver (UI + CLI + tests) or a swappable backend. — https://alistair.cockburn.us/hexagonal-architecture/
- **Dependency inversion is how you keep the rule when control flow goes outward.** The high-level module owns the interface; the low-level module implements it, so the compile-time dependency flips while runtime flow is unchanged. — https://learn.microsoft.com/ja-jp/dotnet/architecture/modern-web-apps-azure/architectural-principles (JP; EN original: https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles)
- **Business rules should live in a unit that depends on no other project unit** (MS guidance: 「ビジネス ルールとロジックは、アプリケーション内の他のプロジェクトに依存しない別のプロジェクトに存在する必要がある」). — same MS Learn URL.
- **Cycles between components are the main thing that kills modularity in practice.** Shopify found "almost every component depended on over half of all the other components" and removed cycles with dependency inversion and publish/subscribe. Make "no cycles between top-level modules" the first checkable rule. — https://shopify.engineering/shopify-monolith

### Package-by-feature vs package-by-layer

- **Small app: layers are fine; when a layer gets big, split the top level by domain and layer inside each domain module.** Fowler: presentation-domain-data separation "should only be applied at a relatively small granularity"; "once any of these layers gets too big you should split your top level into domain oriented modules which are internally layered." — https://martinfowler.com/bliki/PresentationDomainDataLayering.html
- **The top-level folder names should say what the system does, not which framework it uses** ("Screaming Architecture": do they "scream: Health Care System ... Or do they scream: Rails, or Spring/Hibernate"). A useful review check for any proposed tree. — https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html
- JP practice reports the same trade-off for front-ends (`src/features/<feature>/{ui,hooks,types}`): a change stays inside one feature folder (secondary source, practitioner blog). — https://zenn.dev/pandanoir/articles/d74d317f2b3caf

### When to extract a module (and when not to)

- **Rule of three, not two.** Don Roberts via Fowler's *Refactoring* (1999): "The first time you do something, you just do it. The second time ... you wince at the duplication, but you do the duplicate thing anyway. The third time you do something similar, you refactor." Primary source is the book (not online); quote verified via secondary: https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming). **Note:** the brief's "extract when a second consumer appears" is *not* what this source says; the canonical threshold is the third occurrence. A second consumer is a reason to *consider* extraction, not a trigger.
- **A wrong abstraction costs more than duplication.** "duplication is far cheaper than the wrong abstraction"; remedy when it is wrong: re-inline into callers and delete what each caller does not need. — https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
- MS Learn states the same caution under DRY: do not merge code that is only coincidentally repeated (「重複は、不適切な抽象化に結びつけるよりも常に望ましい」). — https://learn.microsoft.com/ja-jp/dotnet/architecture/modern-web-apps-azure/architectural-principles
- **YAGNI covers speculative modules/layers, not refactoring.** "Yagni only applies to capabilities built into the software to support a presumptive feature, it does not apply to effort to make the software easier to modify." Presumptive structure has a "cost of carry". — https://martinfowler.com/bliki/Yagni.html
- **Size of the decision effort should scale with the system.** Hiroki Daichi (JP, 2020): for ~10k-line software the share of time spent on up-front risk resolution is small; at 10M lines it can approach half. Direct dependencies toward the layers that change slowly ("pace layering"); treat frameworks as sticky (hard to reverse) and libraries as swappable. — https://qiita.com/hirokidaichi/items/a746062917595619720b

### Bounded contexts at small scale

- **Split where the language changes.** "you need a different model when the language changes"; the same word (Fowler's "meter" example) meaning different things in two areas is the signal for a boundary. Human culture dominates over technical factors. — https://martinfowler.com/bliki/BoundedContext.html
- Each bounded context ideally owns its own names and its own persistence; contexts talk through program interfaces, not a shared database. — https://learn.microsoft.com/ja-jp/dotnet/architecture/modern-web-apps-azure/architectural-principles

### Modular monolith vs services

- **Start with a monolith.** "Almost all the successful microservice stories have started with a monolith that got too big and was broken up"; services built from scratch mostly "ended up in serious trouble"; "even experienced architects working in familiar domains have great difficulty getting boundaries right at the beginning." — https://martinfowler.com/bliki/MonolithFirst.html
- **Services buy strong boundaries, independent deploy and tech diversity; they cost distribution, eventual consistency and operational complexity** (the "microservice premium"). For a small team, the benefit (strong boundaries) can be had in-process with enforced module rules (section 5). — https://martinfowler.com/articles/microservice-trade-offs.html
- **Extract a service only for a named reason** (Shopify: high-throughput read-only storefront rendering, card-data isolation); otherwise keep components inside the monolith with public interfaces and static boundary checks (Packwerk). — https://shopify.engineering/shopify-monolith

### When NOT to split (small projects)

- One package / one command at the root is Go's own first recommended layout; add `internal/` and more packages only as the project grows. — https://go.dev/doc/modules/layout
- Layering is fine at small size; switch to domain modules only when a layer "gets too big". — https://martinfowler.com/bliki/PresentationDomainDataLayering.html
- Do not build structure for presumptive features (YAGNI). — https://martinfowler.com/bliki/Yagni.html

---

## 2. Folder structure conventions per ecosystem

### Python

- **src layout vs flat layout — PyPA describes, does not mandate.** src layout "helps prevent accidental usage of the in-development copy of the code" and ensures an editable install only imports files meant to be importable; cost: it "requires installation of the project to be able to run its code" (a CLI cannot run straight from the tree). The PyPA page itself stays neutral. — https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- **pytest does recommend src layout for new projects**: "it is **strongly** suggested to use a `src` layout", tests in a directory outside the application code, and "For new projects, we recommend to use `importlib`" import mode. — https://docs.pytest.org/en/stable/explanation/goodpractices.html
- Decision rule for the skill: library or anything installable → `src/<pkg>/` + `tests/`; single-file script or throwaway tool → flat is acceptable (PyPA's trade-off above).

### Swift (packages and Xcode apps)

- **SwiftPM default layout**: `Sources/<TargetName>/` for targets ("By default, the Swift Package Manager requires a target's sources to reside at predefined search paths; for example, `[PackageRoot]/Sources/[TargetName]`"). — https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html
- Test targets default to `Tests/<TargetName>/`: SwiftPM source defines `predefinedTestDirectories = ["Tests", "Sources", "Source", "src", "srcs"]` and `predefinedSourceDirectories = ["Sources", "Source", "src", "srcs"]`. — https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageLoading/PackageBuilder.swift
- **Modularize an Xcode app with local packages.** Apple: "organize its code in a modular way to keep it maintainable by creating Swift packages and using them as local packages"; good first candidates are "networking logic, source files that contain utilities"; later a local package can move to its own repo for reuse. — https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages
- **A target is a real boundary in Swift**: the default access level is `internal` (visible only inside the module), and the `package` modifier (SE-0386, implemented in Swift 5.9) exposes symbols to other targets of the same package without making them `public`. So SPM targets enforce dependency direction at compile time. — https://github.com/swiftlang/swift-book/blob/main/TSPL.docc/LanguageGuide/AccessControl.md , https://github.com/swiftlang/swift-evolution/blob/main/proposals/0386-package-access-modifier.md
- Feature folders inside a SwiftUI app target (e.g. `Features/<Feature>/`): no Apple primary source found that prescribes this. **(unverified as an official convention — community practice only.)**

### Go

- **Official guide: start at the smallest layout that works.** Basic package or basic command in the module root; supporting packages under `internal/`; multiple commands each in their own directory; for a server, "keep all Go commands together in a `cmd` directory" and "keep the Go packages implementing the server's logic in the `internal` directory." — https://go.dev/doc/modules/layout
- **`internal/` is compiler-enforced**: "An import of a path containing the element "internal" is disallowed if the importing code is outside the tree rooted at the parent of the "internal" directory." — https://pkg.go.dev/cmd/go#hdr-Internal_Directories
- **Do not cite `golang-standards/project-layout` as a standard.** Russ Cox (Go tech lead) in issue #117 (2021-04-09): "The _vast_ majority of packages in the Go ecosystem do _not_ put the importable packages in a `pkg` subdirectory"; "what is described here is just very complex, and Go repos tend to be much simpler"; "It is unfortunate that this is being put forth as 'golang-standards' when it really is not." — https://github.com/golang-standards/project-layout/issues/117

### TypeScript / Node

- **Monorepo = one root package with workspaces.** npm: "Workspaces ... provides support for managing multiple packages from your local file system from within a singular top-level, root package", declared via `"workspaces": ["packages/a"]` in the root `package.json`. — https://docs.npmjs.com/cli/v10/using-npm/workspaces
- pnpm: needs `pnpm-workspace.yaml` at the root; the `workspace:` protocol makes pnpm "refuse to resolve to anything other than a local workspace package" and is rewritten to a real version on publish. — https://pnpm.io/workspaces
- **TypeScript project references** "enforce logical separation between components" and speed builds; referenced projects need `"composite": true`; build with `tsc -b`. Use when the monorepo has package boundaries you want the compiler to respect. — https://www.typescriptlang.org/docs/handbook/project-references.html
- Feature folders inside one app: see section 1 (Fowler, Screaming Architecture; JP practice note).

### Generic rules

- Tests in a separate `tests/` tree (pytest recommendation above; SwiftPM `Tests/`); Go is the exception — `_test.go` files sit beside the code (shown in every layout on https://go.dev/doc/modules/layout).
- Keep executables/entry points separate from logic (`cmd/` in Go; the same idea as ports/adapters driving the core). — https://go.dev/doc/modules/layout , https://alistair.cockburn.us/hexagonal-architecture/
- `scripts/` and `docs/` locations: no primary cross-ecosystem source found. **(unverified — convention only; follow the ecosystem's tooling.)**

### File-size / god-file heuristics (verified defaults)

| Tool | Rule | Default | Source |
|---|---|---|---|
| SwiftLint | `file_length` | warning 400, error 1000 lines; `ignore_comment_only_lines: false` | https://realm.github.io/SwiftLint/file_length.html |
| ESLint | `max-lines` | 300 lines; `skipBlankLines` / `skipComments` off unless set | https://eslint.org/docs/latest/rules/max-lines , source: https://github.com/eslint/eslint/blob/main/lib/rules/max-lines.js |
| Pylint | `too-many-lines` (C0302) / `max-module-lines` | 1000 lines (also `max-args` 5, `max-branches` 12, `max-statements` 50, `max-line-length` 100) | https://pylint.readthedocs.io/en/stable/user_guide/messages/convention/too-many-lines.html ; defaults read from `pylint --generate-toml-config`, pylint 4.0.9 (the docs page does not print the default) |

- These numbers are tool defaults, not research findings; treat them as a starting ceiling the user can change in the ratified doc.

---

## 3. Main technology choices

### Dimensions to compare

- **Maturity / known failure modes.** McKinley: boring tech has known unknowns ("we don't know what happens when this database hits 100% CPU") instead of unknown unknowns. — https://mcfunley.com/choose-boring-technology
- **Innovation budget.** "Every company gets about three innovation tokens." Count how many new technologies a proposal spends. — same URL.
- **Operational cost of every added technology.** "You have to monitor the thing. You have to figure out unit tests. You need to know the first thing about it to hack on it." "The long-term costs of keeping a system working reliably vastly exceed any inconveniences you encounter while building it." — same URL.
- **Process before adding something new**: ask "How would you solve your immediate problem without adding anything new?" and write down "exactly what it is about the current stack that makes solving the problem prohibitively expensive." — same URL.
- **Reversibility / lock-in**: frameworks are sticky (「フレームワークの依存性における粘着性の高さ」), libraries are swappable; decide the sticky ones with more care. — https://qiita.com/hirokidaichi/items/a746062917595619720b
- **Maturity rings as vocabulary.** Thoughtworks Radar rings: Adopt ("no doubt that it's proven and mature for use"), Trial ("ready for use, but not as completely proven"), Assess ("worth keeping an eye on"), and a fourth ring the current FAQ calls **Caution** (formerly "Hold"): "may be accepted in the industry, [but] we haven't had a good experience with". — https://www.thoughtworks.com/radar/faq . Build-your-own-radar exists to "balance the risk in your technology portfolio". — https://www.thoughtworks.com/radar/byor
- Team familiarity: covered implicitly by McKinley's "known unknowns" and operational-knowledge points; no separate primary source gathered. Licensing: no primary decision-criteria source gathered in this pass **(unverified as a sourced heuristic; still include it as a dimension)**.

### Recording and presenting options

- **ADR (Nygard)**: Title, Context ("the forces at play ... technological, political, social, and project local"), Decision (active voice), Status (proposed / accepted / deprecated / superseded), Consequences ("All consequences should be listed here"); one or two pages; superseded ADRs are kept and marked. — https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- **For 2+ options use MADR's shape**: Context and Problem Statement → Decision Drivers → Considered Options → Decision Outcome (+ Consequences: "Good, because … / Bad, because …") → Pros and Cons of the Options (per option: Good / Neutral / Bad, because …). — https://github.com/adr/madr/blob/develop/template/adr-template.md
- Practical shape for the skill: list the decision drivers first (from section 3 dimensions), then each option's Good/Bad against those same drivers, then the recommendation and what would make it wrong.

---

## 4. CI baseline stages

- **CI principles to keep the baseline honest**: self-testing build; fix a broken build first ("nobody has a higher priority task than fixing the build"); keep the build fast (the ten-minute build). — https://martinfowler.com/articles/continuousIntegration.html
- **Minimal stages (Python example from GitHub docs)**: `setup-python` with dependency caching → lint (Ruff) → tests (pytest, JUnit + coverage output); optional version matrix. — https://docs.github.com/en/actions/tutorials/build-and-test-code/python
- **Swift package**: `swift build` + `swift test`, runnable on Ubuntu or macOS runners. — https://docs.github.com/en/actions/tutorials/build-and-test-code/swift
- **Suggested growth order for a small project** (synthesis of the sources above, not a single source's list): (1) format/lint + unit tests + build/type-check on every PR → (2) architecture-rule check (section 5) as a normal test → (3) dependency updates (Dependabot) and security scanning → (4) release automation.
- **Dependency updates**: Dependabot version updates via a checked-in `.github/dependabot.yml`. — https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates
- **Security scanning is free on public repos, paid on private.** Code scanning and secret scanning are on by default for public repos; private repos need GitHub Code Security (code scanning, dependency review) or GitHub Secret Protection. — https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security . Dependency review "scans for vulnerable versions of dependencies introduced by package version changes in pull requests"; available on all public repos, private needs Code Security / Advanced Security. — https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review

### Cost: macOS runners (matters for Xcode projects)

- Standard hosted runners are free for public repos and self-hosted runners are free: "GitHub Actions usage is free for self-hosted runners and for public repositories that use standard GitHub-hosted runners." Included minutes: Free 2,000/month; Pro and Team 3,000/month. — https://docs.github.com/en/billing/concepts/product-billing/github-actions
- Per-minute rates: Linux 2-core x64 $0.006, Windows 2-core $0.010, **macOS 3/4-core $0.062** (about 10x Linux). — https://docs.github.com/en/billing/reference/actions-runner-pricing
- Alternative for Apple apps: Xcode Cloud includes **25 compute hours/month** with Apple Developer Program membership; paid tiers from 100 h for US$49.99/month. — https://developer.apple.com/xcode-cloud/
- Implication for a private Xcode project: run `swift test` for pure-logic packages on Linux where it compiles (cheap), and keep macOS jobs for the app target only.

### Local-first alternatives

- **pre-commit**: "a framework for managing and maintaining multi-language pre-commit hooks"; the same hooks run in CI with `pre-commit run --all-files`; pre-commit.ci is a hosted option. — https://pre-commit.com/
- Makefile / task-runner as the single entry point that CI also calls: no primary source gathered **(unverified as a sourced practice; common convention)**.

---

## 5. Checkable architecture rules (fitness functions)

- **Concept**: "Fitness functions describe how close an architecture is to achieving an architectural aim" — tests that measure alignment to architectural goals, run like TDD. — https://www.thoughtworks.com/insights/articles/fitness-function-driven-development

| Ecosystem | Tool | What it checks | Source |
|---|---|---|---|
| Python | import-linter (`lint-imports`) | Contracts in `.importlinter` (or pyproject): Forbidden, Protected, Layers, Independence, Acyclic siblings, custom | https://import-linter.readthedocs.io/en/stable/ |
| JS/TS | dependency-cruiser (`npx dependency-cruiser --init`, then `depcruise`) | Validates dependencies against your rules; default config includes no-circular, orphans, prod-depends-on-dev; ESLint-like output for CI | https://github.com/sverweij/dependency-cruiser |
| JS/TS | TypeScript project references | Compiler-enforced separation between referenced projects | https://www.typescriptlang.org/docs/handbook/project-references.html |
| JVM | ArchUnit | Unit tests over bytecode: `layeredArchitecture().layer(...).whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")`; `slices().matching("..myapp.(*)..").should().beFreeOfCycles()` | https://www.archunit.org/userguide/html/000_Index.html |
| Go | `internal/` directories | Compiler-enforced import restriction | https://pkg.go.dev/cmd/go#hdr-Internal_Directories |
| Go | depguard (via golangci-lint) | Per-file-glob allow/deny import lists (`$gostd`, `$all`, `$test`) | https://golangci-lint.run/docs/linters/configuration/ |
| Go | gomodguard (via golangci-lint) | Allow/block direct module dependencies | https://golangci-lint.run/docs/linters/configuration/ |
| Swift | SPM targets + access control | Separate targets make `internal` symbols invisible across the boundary; declared `dependencies:` define allowed direction | https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html , https://github.com/swiftlang/swift-evolution/blob/main/proposals/0386-package-access-modifier.md |
| Swift | SwiftLint `custom_rules` | Regex rules with optional `included` / `excluded` path regexes (e.g. forbid `import Networking` under a UI path) | https://github.com/realm/SwiftLint/blob/main/README.md (Regex Custom Rules section) |
| Swift | Harmonize | "lint rules as unit tests" over code structure (XCTest-style assertions, e.g. all `*ViewModel` classes inherit a base) | https://github.com/perrystreetsoftware/Harmonize |
| Ruby | Packwerk | Static boundary checks between components of a modular monolith | https://shopify.engineering/shopify-monolith |

- **`go vet` is not a boundary tool**: its analyzers (printf, copylocks, structtag, …) include no import-restriction check; use `internal/` or depguard instead. — https://pkg.go.dev/cmd/vet
- Recommended first rules for any project (derived from sections 1 and 5): (1) no cycles between top-level modules; (2) the core/domain module imports no adapter/UI/infra module; (3) only the composition root (app entry / `cmd/`) imports everything. Each maps directly onto a Layers/Independence contract, a dependency-cruiser `forbidden` rule, an ArchUnit layer rule, or SPM target dependencies.

---

## Not verified / gaps

- "Extract a module when a second consumer appears": no primary source found; the sourced threshold is the rule of three (third occurrence).
- *Refactoring* (1999) rule-of-three quote: verified only through a secondary source (Wikipedia); the book is not online.
- Feature folders as an Apple-endorsed SwiftUI convention: not found in Apple docs.
- `scripts/`, `docs/`, Makefile-as-entry-point conventions: no primary source gathered.
- Licensing as a tech-choice dimension: no primary decision-criteria source gathered.
- Harmonize maintenance status / latest release date: not confirmed.
- Pylint numeric defaults come from running pylint 4.0.9 locally; the online docs page does not print them.
- Traditional Chinese sources: none added; EN and JP primary sources covered every area.

## Sources

- Clean Architecture — https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- Screaming Architecture — https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html
- Hexagonal Architecture — https://alistair.cockburn.us/hexagonal-architecture/
- MS Learn アーキテクチャの原則 — https://learn.microsoft.com/ja-jp/dotnet/architecture/modern-web-apps-azure/architectural-principles
- Fowler, PresentationDomainDataLayering — https://martinfowler.com/bliki/PresentationDomainDataLayering.html
- Fowler, BoundedContext — https://martinfowler.com/bliki/BoundedContext.html
- Fowler, MonolithFirst — https://martinfowler.com/bliki/MonolithFirst.html
- Fowler, Microservice Trade-Offs — https://martinfowler.com/articles/microservice-trade-offs.html
- Fowler, Yagni — https://martinfowler.com/bliki/Yagni.html
- Fowler, Continuous Integration — https://martinfowler.com/articles/continuousIntegration.html
- Rule of three (secondary) — https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)
- Sandi Metz, The Wrong Abstraction — https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
- Shopify modular monolith — https://shopify.engineering/shopify-monolith
- 広木大地, 技術選定/アーキテクチャ設計で後悔しないためのガイドライン — https://qiita.com/hirokidaichi/items/a746062917595619720b
- package by feature のススメ (practitioner) — https://zenn.dev/pandanoir/articles/d74d317f2b3caf
- PyPA src vs flat — https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- pytest good practices — https://docs.pytest.org/en/stable/explanation/goodpractices.html
- SwiftPM PackageDescription — https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html
- SwiftPM PackageBuilder source — https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageLoading/PackageBuilder.swift
- Apple, Organizing your code with local packages — https://developer.apple.com/documentation/xcode/organizing-your-code-with-local-packages
- Swift access control — https://github.com/swiftlang/swift-book/blob/main/TSPL.docc/LanguageGuide/AccessControl.md
- SE-0386 package access modifier — https://github.com/swiftlang/swift-evolution/blob/main/proposals/0386-package-access-modifier.md
- Go, Organizing a Go module — https://go.dev/doc/modules/layout
- Go internal directories — https://pkg.go.dev/cmd/go#hdr-Internal_Directories
- golang-standards/project-layout issue #117 — https://github.com/golang-standards/project-layout/issues/117
- go vet — https://pkg.go.dev/cmd/vet
- npm workspaces — https://docs.npmjs.com/cli/v10/using-npm/workspaces
- pnpm workspaces — https://pnpm.io/workspaces
- TypeScript project references — https://www.typescriptlang.org/docs/handbook/project-references.html
- SwiftLint file_length — https://realm.github.io/SwiftLint/file_length.html
- SwiftLint README (custom rules) — https://github.com/realm/SwiftLint/blob/main/README.md
- ESLint max-lines — https://eslint.org/docs/latest/rules/max-lines
- Pylint too-many-lines — https://pylint.readthedocs.io/en/stable/user_guide/messages/convention/too-many-lines.html
- Choose Boring Technology — https://mcfunley.com/choose-boring-technology
- Thoughtworks Radar FAQ — https://www.thoughtworks.com/radar/faq
- Thoughtworks Build your own Radar — https://www.thoughtworks.com/radar/byor
- Nygard, Documenting Architecture Decisions — https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- MADR template — https://github.com/adr/madr/blob/develop/template/adr-template.md
- GitHub Actions Python — https://docs.github.com/en/actions/tutorials/build-and-test-code/python
- GitHub Actions Swift — https://docs.github.com/en/actions/tutorials/build-and-test-code/swift
- GitHub Actions billing — https://docs.github.com/en/billing/concepts/product-billing/github-actions
- GitHub runner pricing — https://docs.github.com/en/billing/reference/actions-runner-pricing
- GitHub Advanced Security — https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security
- Dependency review — https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review
- Dependabot version updates — https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates
- Xcode Cloud — https://developer.apple.com/xcode-cloud/
- pre-commit — https://pre-commit.com/
- Thoughtworks, Fitness function-driven development — https://www.thoughtworks.com/insights/articles/fitness-function-driven-development
- import-linter — https://import-linter.readthedocs.io/en/stable/
- dependency-cruiser — https://github.com/sverweij/dependency-cruiser
- ArchUnit user guide — https://www.archunit.org/userguide/html/000_Index.html
- golangci-lint linter configuration (depguard, gomodguard) — https://golangci-lint.run/docs/linters/configuration/
- Harmonize — https://github.com/perrystreetsoftware/Harmonize
