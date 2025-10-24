# Modular CV Builder

A lightweight Python CLI for managing CV content as reusable, bilingual (EN/KR) components.

## Quick Start

```bash
# Build CVs
poetry run python -m cv_builder.cli --profile full-en
poetry run python -m cv_builder.cli --profile full-kr

# Validate
poetry run python -m cv_builder.cli --profile full-en --validate-only

# Render to PDF
poetry run rendercv render Jaepil_Choi_CV_en.yaml
```

## Overview

**What it does:**
- Stores each work experience/project as individual bilingual YAML files
- Composes different CV variants by selecting items via profiles
- Tracks character counts for page optimization
- Validates structure, dates, and bilingual completeness
- Outputs RenderCV-compatible YAMLs

**Directory structure:**
```
modular_cv/
├── cv_items/
│   ├── work_experience/     # Individual items
│   │   ├── .metadata/       # Auto-generated metadata
│   │   │   ├── meritz-macro-trading.yaml
│   │   │   └── ...
│   │   ├── meritz-macro-trading.yaml
│   │   └── ...
│   └── projects/
│       ├── .metadata/       # Auto-generated metadata
│       │   └── ...
│       ├── krx-quant-dataloader.yaml
│       └── ...
├── profiles/               # Selection specs
│   ├── full-en.yaml
│   ├── full-kr.yaml
│   └── quant-focused-en.yaml
└── base/                   # Templates (header/design/locale)
    ├── base_en.yaml
    └── base_kr.yaml
```

## Data Model

### Work Experience Item

**Item file** (`cv_items/work_experience/company-role-slug.yaml`):
```yaml
id: company-role-slug
type: work_experience
tags: [quant, trading, python]
priority: 1  # Lower = appears first
data:
  company: {en: "Company", kr: "회사명"}
  position: {en: "Title - duration", kr: "직책 - 기간"}
  start_date: "2025-01"
  end_date: "2025-07"  # or "present"
  location: {en: "Seoul, South Korea", kr: "서울, 대한민국"}
  highlights:
    - {en: "Achievement 1", kr: "성과 1"}
    - {en: "Achievement 2", kr: "성과 2"}
```

**Metadata file** (`cv_items/work_experience/.metadata/company-role-slug.yaml`) - **auto-generated**:
```yaml
char_count: {en: 493, kr: 216}
```

### Project Item

**Item file** (`cv_items/projects/project-slug.yaml`):
```yaml
id: project-slug
type: project
tags: [python, open-source]
priority: 1
data:
  name: {en: "[Name](url)", kr: "[이름](url)"}
  highlights:
    - {en: "Feature 1", kr: "기능 1"}
```

**Metadata file** (`cv_items/projects/.metadata/project-slug.yaml`) - **auto-generated**:
```yaml
char_count: {en: 347, kr: 207}
```

### Profile

```yaml
name: profile-name
locale: en  # or kr
base_file: base_en.yaml
sections:
  Work Experience:
    include_ids: [meritz-macro-trading, zero-one-ai, ...]
    max_items: 5
  Projects:
    include_ids: [krx-quant-dataloader, qtrsch]
    max_items: 3
output_file: Jaepil_Choi_CV_en.yaml
```

## Common Tasks

### Add New Work Experience

1. Create `modular_cv/cv_items/work_experience/{id}.yaml` with bilingual content (no metadata section needed)
2. Run: `poetry run python scripts/update_char_counts.py` to auto-generate metadata file
3. Add `{id}` to relevant profile `include_ids`
4. Rebuild: `poetry run python -m cv_builder.cli --profile full-en`

### Create Focused CV Variant

1. Create `modular_cv/profiles/quant-focused-en.yaml`
2. Select 3-4 relevant work experiences + 2-3 projects
3. Build: `poetry run python -m cv_builder.cli --profile quant-focused-en`

### Update Existing Item

1. Edit item YAML (update both EN and KR)
2. Run: `poetry run python scripts/update_char_counts.py` to recalculate character counts
3. Validate: `poetry run python -m cv_builder.cli --profile full-en --validate-only`
4. Rebuild affected profiles

## Validation

The builder checks:
- Required fields present
- Date format (`YYYY-MM`) and logic (`start_date <= end_date`)
- Bilingual completeness (both `en` and `kr` in all text fields)
- Unique item IDs
- Profile references existing items

## Character Count Tracking

**Build output shows:**
```
Character count statistics:
  Work Experience: 1969 chars (5 items)
  Projects: 1071 chars (3 items)
Total: 3040 chars
```

**Guidelines:**
- **1 page**: ~2500-3000 total chars (3-4 work exp + 2-3 projects)
- **2 pages**: ~5000-6000 total chars (all content)

## Example Use Cases

### Scenario 1: Quant Trading Application (1-page)
```yaml
# modular_cv/profiles/quant-focused-en.yaml
sections:
  Work Experience:
    include_ids: [meritz-macro-trading, zero-one-ai, haafor-research]
  Projects:
    include_ids: [krx-quant-dataloader, qtrsch]
# Result: ~1987 chars, fits on 1 page
```

### Scenario 2: Full Korean CV
```yaml
# modular_cv/profiles/full-kr.yaml
sections:
  Work Experience:
    include_ids: [all 5 items]
  Projects:
    include_ids: [all 3 items]
# Result: ~1519 chars (Korean is ~50% more concise than English)
```

## CLI Commands

```bash
# Update character counts (run after editing items)
poetry run python scripts/update_char_counts.py

# Build CV
poetry run python -m cv_builder.cli --profile PROFILE_NAME

# Validate only
poetry run python -m cv_builder.cli --profile PROFILE_NAME --validate-only

# Custom output
poetry run python -m cv_builder.cli --profile PROFILE_NAME --output path/to/cv.yaml

# Help
poetry run python -m cv_builder.cli --help
```

## Tips

1. **Use descriptive IDs**: `company-role` not `job1`
2. **Set priorities strategically**: Lower number = higher priority (appears first)
3. **Tag items**: Prepare for future tag-based filtering (`quant`, `trading`, `ml`, etc.)
4. **Keep translations synced**: Always update both EN and KR
5. **Validate before building**: Use `--validate-only` first
6. **Test render**: Always verify PDF with `poetry run rendercv render output.yaml`

## System Architecture

```
CV Items (content) + Profiles (selection) + Base (template)
    ↓
CV Builder CLI
    ↓ (Load → Validate → Select → Compose)
RenderCV YAML
    ↓ (RenderCV)
PDF / PNG / HTML
```

**Modules:**
- `cv_builder/models.py` - Data structures
- `cv_builder/loader.py` - YAML I/O
- `cv_builder/validator.py` - Validation logic
- `cv_builder/composer.py` - Composition & character counting
- `cv_builder/cli.py` - CLI interface

## Troubleshooting

**Error: Profile not found**
- Check profile name (no `.yaml` extension in command)

**Error: Item validation failed**
- Verify all required fields present
- Check bilingual completeness (both `en` and `kr`)
- Validate date format (`YYYY-MM`)

**Error: Unknown item ID**
- Check spelling in profile `include_ids`
- Verify item file exists and `id` field matches filename

## Future Enhancements

Deferred to keep MVP focused:
- Tag-based selection (`include_tags: [quant, trading]`)
- Per-item highlight limits
- Interactive CLI selection
- Content compression for page limits
- Automated RenderCV invocation
- Unit tests & CI

## Current Statistics

**Full English CV (full-en):**
- 5 work experiences + 3 projects = 3040 chars (2 pages)

**Full Korean CV (full-kr):**
- 5 work experiences + 3 projects = 1519 chars (1 page)

**Quant-focused CV (quant-focused-en):**
- 3 work experiences + 2 projects = 1987 chars (1 page)

All profiles tested and working with RenderCV.
