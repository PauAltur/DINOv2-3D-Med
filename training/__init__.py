"""Training module for DINOv2-3D."""

from .dinov2_lightning_module import DINOv2_3D_LightningModule
from .data_module import DataModule

# Import DINOtxt conditionally to avoid import errors if not used
try:
    from .dinotxt_lightning_module import DINOtxt_LightningModule
    __all__ = [
        "DINOv2_3D_LightningModule",
        "DINOtxt_LightningModule",
        "DataModule",
    ]
except ImportError:
    __all__ = [
        "DINOv2_3D_LightningModule",
        "DataModule",
    ]
