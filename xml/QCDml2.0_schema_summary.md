# QCDml 2.0 Schema Summary: Required vs. Optional Tags

---

## QCDmlConfig2.0.0.xsd — root: `<gaugeConfiguration>`

### Top-level children
| Tag | Required? |
|---|---|
| `dataLFN` | **required** |
| `management` | **required** |
| `implementation` | **required** |
| `algorithm` | **required** |
| `precision` | **required** |
| `markovSequence` | **required** |
| `additionalInfo` | optional |

### `<management>`
| Tag | Required? |
|---|---|
| `annotation` | optional |
| `revisions` | optional |
| `reference` | optional |
| `archiveHistory` | **required** |
| → `archiveEvent` (1+) | **required** |
| → → `annotation` | optional |
| → → `revision` | optional |
| → → `revisionAction` | **required** |
| → → `participant` | **required** |
| → → `date` | **required** |

`participant` is a **choice**: either `orcid` (required) with optional `name`/`institution`, or `name` + `institution` (both required, no orcid).

### `<implementation>`
| Tag | Required? |
|---|---|
| `annotation` | optional |
| `machine/annotation` | optional |
| `machine/name` | **required** |
| `machine/institution` | **required** |
| `machine/machineType` | **required** |
| `code/annotation` | optional |
| `code/name` | **required** |
| `code/version` | **required** |
| `code/date` | **required** |

### `<algorithm>`
| Tag | Required? |
|---|---|
| `annotation` | optional |
| `parameters` | optional |
| → `parameter` (0+) | optional |
| → → `annotation` | optional |
| → → `name` | **required** |
| → → `value` | **required** |
| `xs:any` (other namespace) | optional |

### `<markovSequence>`
| Tag | Required? |
|---|---|
| `annotation` | optional |
| `markovChainURI` | **required** |
| `series` | **required** |
| `markovStep` (1+) | **required** |
| → `annotation` | optional |
| → `update` | **required** |
| → `record` (1+) | **required** |
| → → `field` | **required** |
| → → `crcCheckSum` | **required** |
| → → `avePlaquette` | **required** |

---

## QCDmlEnsemble2.0.0.xsd — root: `<markovChain>`

### Top-level children
| Tag | Required? |
|---|---|
| `markovChainURI` | **required** |
| `management` | **required** |
| `license` | **required** |
| `fundingReferences` | optional |
| `physics` | **required** |
| `algorithm` | **required** |
| `cLibrary` | optional |
| `additionalInfo` | optional |

### `<management>`
| Tag | Required? |
|---|---|
| `annotation` | optional |
| `revisions` | optional |
| `collaboration` | **required** |
| `projectName` | **required** |
| `ensembleLabel` | optional |
| `publishedAlias` | optional |
| `reference` | optional |
| `archiveHistory` | **required** |
| → `archiveEvent` (0+) | optional |

`archiveEvent` has the same internal structure as in the Config schema (annotation, revision optional; revisionAction, participant, date required).

### `<license>`
| Tag | Required? |
|---|---|
| `annotation` | optional |
| `licenseName` | optional (standard license only) |
| `licenseURI` | **required** (standard license) OR |
| `customLicenseText` | **required** (custom license, unless reference-only) |
| `customLicenseReference` | optional (or required if text-less custom license) |
| `embargoEndDate` | optional |
| `acknowledgments` | optional |
| → `annotation` | optional |
| → `citation` (1+) | **required** (if not using templateText alone) |
| → `templateText` | optional (or required if no citation) |

### `<fundingReferences>` (optional block; if present, must contain at least one `fundingReference`)
| Tag | Required? |
|---|---|
| `annotation` | optional |
| `fundingReference` (1+) | **required** |
| → `annotation` | optional |
| → `funderName` | **required** |
| → `awardTitle` | optional |
| → `awardNumber` | optional |

### `<physics>`
| Tag | Required? |
|---|---|
| `annotation` | optional |
| `size` | **required** |
| → `annotation` | optional |
| → `x`, `t` | **required** |
| → `y`, `z` | optional (omit for lower-dimensional simulations) |
| `action` | **required** |
| → `annotation` | optional |
| → `gluon` | **required** |
| → `photon` | optional |
| → `quark` | optional |
| `observables` | optional |

### `<algorithm>`
| Tag | Required? |
|---|---|
| `annotation` | optional |
| `name` | **required** |
| `glossary` | **required** |
| `reference` | **required** |
| `exact` | **required** |
| `reweightingNeeded` | **required** |
| `parameters` | optional |
| `xs:any` (other namespace) | optional |

---

## Key Differences Between the Two Schemas

- The **Ensemble** schema has `collaboration`, `projectName`, `license`, `fundingReferences`,
  `physics`, and a richer `algorithm` block — none of which appear in the Config schema.
- The **Config** schema has `implementation`, `precision`, and `markovSequence`
  (with per-configuration `markovStep`/`record` data) — not in the Ensemble schema.
- `archiveEvent` is **required** (1 or more) in Config but **optional** (0 or more) in Ensemble.
