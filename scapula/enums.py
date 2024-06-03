from enum import Enum

import numpy as np

from .scapula_generic import ScapulaJcsGeneric


class ScapulaDataType(Enum):
    RAW = 1
    RAW_NORMALIZED = 2
    LOCAL = 3


class JointCoordinateSystem(Enum):
    """
    Enum that defines the joint coordinate systems for the scapula. The coordinate systems are defined by the origin,
    the x-axis and the y-plane.
    """

    ISB = ScapulaJcsGeneric(
        origin=["AA"],
        axis=(["TS"], ["AA"]),
        axis_name="x",
        plane=((["AI"], ["TS"]), (["AI"], ["AA"])),
        plane_name="y",
        keep="axis",
    )
    # SCS2 = ScapulaJcsGeneric(
    #     origin=["AA"],
    #     axis=(["TS"], ["AA"]),
    #     axis_name="x",
    #     plane=((["AI"], ["TS"]), (["AI"], ["AA"])),
    #     plane_name="y",
    #     keep="axis",
    # )
    # SCS3 = ScapulaJcsGeneric(
    #     origin=["AC"],
    #     axis=(["TS"], ["AC"]),
    #     axis_name="x",
    #     plane=((["AI"], ["TS"]), (["AI"], ["AC"])),
    #     plane_name="y",
    #     keep="axis",
    # )
    # SCS4 = ScapulaJcsGeneric(
    #     origin=["GC_CONTOUR"],
    #     axis=(["TS"], ["GC_CONTOUR"]),
    #     axis_name="x",
    #     plane=((["AI"], ["TS"]), (["AI"], ["GC_CONTOUR"])),
    #     plane_name="y",
    #     keep="axis",
    # )
    # SCS5 = ScapulaJcsGeneric(
    #     origin=["TS"],
    #     axis=(["TS"], ["AC"]),
    #     axis_name="x",
    #     plane=((["AI"], ["TS"]), (["AI"], ["AC"])),
    #     plane_name="y",
    #     keep="axis",
    # )
    # SCS6 = ScapulaJcsGeneric(
    #     origin=["AC"],
    #     axis=(["TS"], ["AC"]),
    #     axis_name="x",
    #     plane=((["AI"], ["TS"]), (["AI"], ["AC"])),
    #     plane_name="y",
    #     keep="axis",
    # )
    # SCS7 = ScapulaJcsGeneric(
    #     origin=["GC"],
    #     axis=(["TS"], ["AC"]),
    #     axis_name="x",
    #     plane=((["AI"], ["TS"]), (["AI"], ["AC"])),
    #     plane_name="y",
    #     keep="axis",
    # )
    # SCS8 = # TODO
    # SCS9 = # TODO
    SCS10 = ScapulaJcsGeneric(
        origin=["GC_CONTOUR"],
        axis=(["IE"], ["SE"]),
        axis_name="z",
        plane="GC_CONTOUR_NORMAL",
        plane_name="x",
        keep="plane",
    )

    def __call__(self, landmarks: dict[str, np.array]) -> np.array:
        return self.value.compute_coordinate_system(landmarks)
