
from .arithmetic_intensity import generate_problem as arithmetic_intensity_gen
from .bytes2bits import generate_problem as bytes2bits_gen
from .ram_bandwidth import generate_problem as ram_bandwidth_gen
from .rec_sys_matrix_fact import generate_problem as rec_sys_matrix_fact_gen
from .roofline import generate_problem as roofline_gen


def dispatch_problem(name: str):
    if name == "bytes2bits":
        return bytes2bits_gen()
    if name == "ram_bandwidth":
        return ram_bandwidth_gen()
    if name == "arithmetic_intensity":
        return arithmetic_intensity_gen()
    if name == "roofline":
        return roofline_gen()
    if name == "rec_sys_matrix_fact":
        return rec_sys_matrix_fact_gen()

