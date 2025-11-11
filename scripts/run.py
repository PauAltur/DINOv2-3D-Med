"""
Script to run 3D DINOv2 training or prediction using a YAML config.
- Uses PyTorch Lightning, MONAI, and custom project modules.
- Accepts config file and overrides via CLI (with fire).
"""

import os
from torch.utils.data import DataLoader
from monai.bundle import ConfigParser

import fire
from utils.imports import import_module_from_path
import torch
import monai

torch.serialization.safe_globals([monai.data.meta_tensor.MetaTensor])


def run(mode, config_file: str, **config_overrides):
    """
    Run training or prediction based on the mode parameter.

    Args:
        config_file (str): Path to the configuration file (YAML)
        mode (str): Either "fit" or "predict"
        **config_overrides: Additional configuration overrides (key=value)
    """

    assert mode in ["fit", "predict"], "Unsupported mode"

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
    parser.update(config_overrides)

    # Get evaluated project path (use parsed content so MONAI expressions are resolved)
    project_path = parser.get_parsed_content("project")
    import_module_from_path("project", project_path)

    trainer = parser.get_parsed_content("trainer")
    lightning_module = parser.get_parsed_content("lightning_module")
    data_module = parser.get_parsed_content("data_module")

    getattr(trainer, mode)(lightning_module, data_module)


if __name__ == "__main__":
    # Set environment variables for better performance
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # Run training or prediction
    fire.Fire(run)
