# Environment Variable Configuration - Technical Details

## How It Works

This project uses **MONAI's ConfigParser** (not OmegaConf) to parse YAML configuration files. The environment variable handling is implemented as follows:

### 1. Environment Variables are Read in `scripts/run.py`

```python
# Read environment variables for paths
env_vars = {
    "PROJECT_ROOT": os.environ.get("PROJECT_ROOT"),
    "OUTPUT_DIR": os.environ.get("OUTPUT_DIR"),
    "DATASET_ROOT": os.environ.get("DATASET_ROOT"),
}

parser = ConfigParser()
parser.read_config(config_file)

# Update parser with environment variables
parser.update(env_vars)

parser.parse()
```

### 2. YAML Files Use MONAI ConfigParser Syntax

MONAI ConfigParser uses the `@variable_name` syntax to reference variables. For environment variables with defaults, we use Python ternary expressions:

```yaml
# Syntax: "$@ENV_VAR if @ENV_VAR is not None else 'default_value'"
project: "$@PROJECT_ROOT if @PROJECT_ROOT is not None else '.'"
output_dir: "$@OUTPUT_DIR if @OUTPUT_DIR is not None else './outputs'"
dataset_root: "$@DATASET_ROOT if @DATASET_ROOT is not None else './data'"
```

### 3. Variable References in Config Files

Once defined, these variables can be referenced elsewhere in the YAML using the `@` prefix:

```yaml
trainer:
  logger:
    save_dir: '@output_dir/@run_name'  # Uses the output_dir variable
  callbacks:
    - dirpath: '@output_dir/@run_name'  # Same here
```

## Syntax Comparison

### ❌ Wrong (OmegaConf syntax - not supported)
```yaml
project: "${oc.env:PROJECT_ROOT,.}"
```

### ✅ Correct (MONAI ConfigParser syntax)
```yaml
project: "$@PROJECT_ROOT if @PROJECT_ROOT is not None else '.'"
```

## How Defaults Work

1. **If environment variable is set**: The value from the environment is used
2. **If environment variable is NOT set**: The default value (after `else`) is used

Example:
```yaml
output_dir: "$@OUTPUT_DIR if @OUTPUT_DIR is not None else './outputs'"
```

- With `OUTPUT_DIR=/mnt/data/outputs` → uses `/mnt/data/outputs`
- Without `OUTPUT_DIR` → uses `./outputs`

## Important Notes

1. **Variable Injection**: Environment variables are injected into the ConfigParser via `parser.update(env_vars)` BEFORE parsing
2. **Parsing Order**: 
   - Read config → Update with env vars → Parse → Update with CLI overrides
3. **None Handling**: `os.environ.get()` returns `None` if variable doesn't exist, which triggers the default in the ternary expression
4. **String Evaluation**: The `$` prefix tells ConfigParser to evaluate the expression as Python code

## Testing

To test if environment variables are being parsed correctly:

```powershell
# Set environment variable
$env:OUTPUT_DIR = "C:\my\custom\path"

# Run with verbose output
python -m scripts.run fit --config_file=./configs/train.yaml
```

The logger should show outputs being saved to your custom path.
