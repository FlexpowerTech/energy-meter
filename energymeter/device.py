from dataclasses import dataclass, field
from typing import List

from pymodbus.client import ModbusTcpClient as MBClient


@dataclass
class Register:
    """
    Default register instance.
    """

    name: str
    index: int
    length: int
    data_type: MBClient.DATATYPE


@dataclass
class ModbusDevice:
    """
    Base dataclass that represents a Modbus device.

    param: model (str): Any string that represents a name of the device.
    param: register_map (List[Register]): contains a list of Register instances.
        Accepts the registers in any order.
    param: registers (List[Register]): auto-generated list of Register. Sorted by index value
        and shifted using index_shift parameter.
    param: unit (int): Modbus slave ID.
    param: index_shift (int): the value by which to shift the indices.
    """

    model: str
    registers_map: List[Register]
    registers: List[Register] = field(init=False)
    unit: int
    index_shift: int = 0

    def __post_init__(self):
        """
        Generate self.register list from self.registers_map.
        Auto-sort by indices ASC and apply auto-shift.
        """
        # Apply index shift and order registers by index asc
        registers = sorted(self.registers_map, key=lambda x: x.index)
        self.__apply_index_shift(registers, self.index_shift)
        self.registers = registers

    def __apply_index_shift(self, registers: List[Register], index_shift: int):
        """
        Shift the indices by specified value.
        """
        for register in registers:
            register.index = register.index + index_shift
