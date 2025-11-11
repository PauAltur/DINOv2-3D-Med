# Path Configuration Changes Summary

## Overview
All hardcoded paths in the configuration files have been replaced with environment variables to make the project portable and easier to configure.

## Changes Made

### 1. Config Files Updated

**Note**: The configuration files use MONAI ConfigParser syntax for environment variables with fallback defaults.

#### `configs/train.yaml`
- **Before**: `project: /home/suraj/Repositories/DINOv2_3D`
- **After**: `project: "$@PROJECT_ROOT if @PROJECT_ROOT is not None else '.'"`

- **Before**: `save_dir: '/mnt/data1/suraj/dinov2_experiments/dinov2_pretrain/@run_name'`
- **After**: `save_dir: '@output_dir/@run_name'`

- **Before**: `dirpath: '/mnt/data1/suraj/dinov2_experiments/dinov2_pretrain/@run_name'`
- **After**: `dirpath: '@output_dir/@run_name'`

- **Added**: `output_dir: "$@OUTPUT_DIR if @OUTPUT_DIR is not None else './outputs'"`

#### `configs/predict.yaml`
- **Before**: `project: /home/suraj/Repositories/DINOv2_3D`
- **After**: `project: "$@PROJECT_ROOT if @PROJECT_ROOT is not None else '.'"`

- **Before**: `path: /home/suraj/Repositories/DINOv2_3D/predictions.csv`
- **After**: `path: "@output_dir/predictions.csv"`

- **Before**: Dataset paths hardcoded to `/mnt/data1/datasets/AMOS/amos22/`
- **After**: `data: "$monai.auto3dseg.datafold_read(f'@dataset_root/AMOS/amos22/dataset.json', basedir=f'@dataset_root/AMOS/amos22', key='validation')[0]"`

- **Added**: 
  - `output_dir: "$@OUTPUT_DIR if @OUTPUT_DIR is not None else './outputs'"`
  - `dataset_root: "$@DATASET_ROOT if @DATASET_ROOT is not None else './data'"`

#### `configs/dinotxt_stage.yaml`
- **Before**: `project: /home/suraj/Repositories/DINOv2_3D`
- **After**: `project: "$@PROJECT_ROOT if @PROJECT_ROOT is not None else '.'"`

- **Before**: `save_dir: '/mnt/data1/suraj/dinov2_experiments/dinov2_pretrain/@run_name'`
- **After**: `save_dir: '@output_dir/@run_name'`

- **Before**: `dirpath: '/mnt/data1/suraj/dinov2_experiments/dinov2_pretrain/@run_name'`
- **After**: `dirpath: '@output_dir/@run_name'`

- **Added**: `output_dir: "$@OUTPUT_DIR if @OUTPUT_DIR is not None else './outputs'"`

#### `configs/datasets/amos.yaml`
- **Before**: `data: "$monai.auto3dseg.datafold_read('/mnt/data1/datasets/AMOS/amos22/dataset.json', basedir='/mnt/data1/datasets/AMOS/amos22', key='training')[0]"`
- **After**: `data: "$monai.auto3dseg.datafold_read(f'@dataset_root/AMOS/amos22/dataset.json', basedir=f'@dataset_root/AMOS/amos22', key='training')[0]"`

- **Added**: `dataset_root: "$@DATASET_ROOT if @DATASET_ROOT is not None else './data'"`

#### `configs/datasets/idc_dump.yaml`
- **Before**: `data: "$monai.auto3dseg.datafold_read('/mnt/ssd1/ibro/IDC_SSL_CT/idc_dump_datalist.json', basedir='', key='training')[0]"`
- **After**: `data: "$monai.auto3dseg.datafold_read(f'@dataset_root/IDC_SSL_CT/idc_dump_datalist.json', basedir='', key='training')[0]"`

- **Added**: `dataset_root: "$@DATASET_ROOT if @DATASET_ROOT is not None else './data'"`

### 2. Run Script Updated

#### `scripts/run.py`
- Added environment variable reading and injection into ConfigParser
- Environment variables (`PROJECT_ROOT`, `OUTPUT_DIR`, `DATASET_ROOT`) are now read from the system and passed to MONAI's ConfigParser before parsing
- This allows the YAML configs to reference these variables using the `@variable_name` syntax

### 2. New Files Created

#### `.env.example`
A template environment file with documentation for all required environment variables:
- `PROJECT_ROOT`: Project root directory (default: `.`)
- `OUTPUT_DIR`: Output directory for experiments, checkpoints, and logs (default: `./outputs`)
- `DATASET_ROOT`: Dataset root directory (default: `./data`)

### 3. Documentation Updated

#### `README.md`
Added a new "Configuration" section explaining:
- How to set up environment variables
- Default values for each variable
- Expected dataset directory structure
- How to override paths

## Environment Variables

The following environment variables are now used:

| Variable | Description | Default Value | Example |
|----------|-------------|---------------|---------|
| `PROJECT_ROOT` | Project root directory | `.` | `/home/user/DINOv2_3D` |
| `OUTPUT_DIR` | Output directory for experiments | `./outputs` | `/mnt/data/experiments` |
| `DATASET_ROOT` | Root directory for datasets | `./data` | `/mnt/data/datasets` |

## Usage

### Option 1: Using .env file (Recommended)
1. Copy `.env.example` to `.env`
2. Edit `.env` with your paths
3. Run training as usual

### Option 2: Set environment variables directly
```bash
# Linux/Mac
export OUTPUT_DIR=/path/to/outputs
export DATASET_ROOT=/path/to/datasets

# Windows PowerShell
$env:OUTPUT_DIR = "C:\path\to\outputs"
$env:DATASET_ROOT = "C:\path\to\datasets"
```

### Option 3: Use defaults
If no environment variables are set, the configuration will use sensible defaults:
- Outputs will be saved to `./outputs/`
- Datasets are expected in `./data/`

## Benefits

1. **Portability**: No more hardcoded paths specific to one user's machine
2. **Flexibility**: Easy to switch between different dataset/output locations
3. **Team-friendly**: Each developer can have their own paths without modifying config files
4. **Git-friendly**: `.env` file can be gitignored, keeping local configurations private
5. **Defaults**: Works out of the box with reasonable defaults if no env vars are set

## Migration Guide

If you have existing data organized with the old paths:

1. Set environment variables to point to your existing locations:
   ```bash
   export DATASET_ROOT=/mnt/data1/datasets
   export OUTPUT_DIR=/mnt/data1/suraj/dinov2_experiments/dinov2_pretrain
   ```

2. Or create a `.env` file with these values

3. Your existing setups will continue to work without moving any data
