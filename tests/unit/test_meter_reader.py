from unittest.mock import Mock

from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian

from energymeter.device import ModbusDevice, Register
from energymeter.reader import ModbusDeviceDataReader


def test_break_down_registers_into_chunks():
    device = ModbusDevice(
        model="Test meter",
        registers_map=[
            Register("value_1", 3000, 2, ModbusTcpClient.DATATYPE.FLOAT32),
            Register("value_2", 3002, 2, ModbusTcpClient.DATATYPE.FLOAT32),
            Register("value_3", 3004, 2, ModbusTcpClient.DATATYPE.FLOAT32),
            Register("value_4", 3200, 2, ModbusTcpClient.DATATYPE.FLOAT32),
            Register("value_5", 3202, 2, ModbusTcpClient.DATATYPE.FLOAT32),
            Register("value_6", 3204, 2, ModbusTcpClient.DATATYPE.FLOAT32),
            Register("value_7", 3250, 2, ModbusTcpClient.DATATYPE.FLOAT32),
            Register("value_8", 3252, 2, ModbusTcpClient.DATATYPE.FLOAT32),
            Register("value_9", 3340, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        ],
        unit=10,
    )

    reader = ModbusDeviceDataReader(
        client=Mock(),
        byteorder=Endian.BIG,
        wordorder=Endian.BIG,
        device=device,
        message_size=100,
    )

    chunks = reader.break_down_registers_into_chunks()

    assert len(chunks) == 3
    chunk_1, chunk_2, chunk_3 = chunks
    assert len(chunk_1) == 3
    assert len(chunk_2) == 5
    assert len(chunk_3) == 1

    assert chunk_1 == device.registers[0:3]
    assert chunk_2 == device.registers[3:8]
    assert chunk_3 == device.registers[8:9]
