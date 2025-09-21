
from .ram_bandwidth import generate_problem as ram_bandwidth_gen
from .bytes2bits import generate_problem as bytes2bits_gen

def dispatch_problem(name: str):
    if name == "bytes2bits":
        return bytes2bits_gen()
    if name == "ram_bandwidth":
        return ram_bandwidth_gen()
