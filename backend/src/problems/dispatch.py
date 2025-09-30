
from .arithmetic_intensity import ArithmeticIntensity
from .batch_norm_problem import BatchNormProblem
from .bytes2bits import Bytes2Bits
from .linear_program_dual import LinearProgramDual
from .ram_bandwidth import RamBandwidth
from .rec_sys_matrix_fact import RecSysMatrixFact
from .roofline import Roofline


def dispatch_problem(name: str):
    if name == "bytes2bits":
        return Bytes2Bits().generate_problem()
    if name == "ram_bandwidth":
        return RamBandwidth().generate_problem()
    if name == "arithmetic_intensity":
        return ArithmeticIntensity().generate_problem()
    if name == "roofline":
        return Roofline().generate_problem()
    if name == "rec_sys_matrix_fact":
        return RecSysMatrixFact().generate_problem()
    if name == "linear_program_dual":
        return LinearProgramDual().generate_problem()
    if name == "batch_norm":
        return BatchNormProblem().generate_problem()
    raise ValueError(f"Unknown problem type: {name}")

