from pymodbus.client.tcp import ModbusTcpClient
from flexmodbusreader.device import ModbusDevice, Register

# Schneider energy meter
# Docs: https://www.se.com/us/en/download/document/PM8000_Modbus_Map/
ExampleMeter = ModbusDevice(
    model="Example Meter Device",
    registers_map=[
        Register("current_phase_a", 3000, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("current_phase_b", 3002, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("current_phase_c", 3004, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("voltage_phase_a", 3028, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("voltage_phase_b", 3030, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("voltage_phase_c", 3032, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("active_power_phase_a", 3054, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("active_power_phase_b", 3056, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("active_power_phase_c", 3058, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("active_power_total", 3060, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("reactive_power_phase_a", 3062, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("reactive_power_phase_b", 3064, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("reactive_power_phase_c", 3066, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("reactive_power_total", 3068, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("apparent_power_phase_a", 3070, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("apparent_power_phase_b", 3072, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("apparent_power_phase_c", 3074, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("apparent_power_total", 3076, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("frequency", 3110, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("active_energy_import", 3204, 4, ModbusTcpClient.DATATYPE.UINT64),
        Register("active_energy_export", 3208, 4, ModbusTcpClient.DATATYPE.UINT64),
        Register("reactive_energy_import", 3220, 4, ModbusTcpClient.DATATYPE.UINT64),
        Register("reactive_energy_export", 3224, 4, ModbusTcpClient.DATATYPE.UINT64),
        Register("apparent_energy_import", 3236, 4, ModbusTcpClient.DATATYPE.UINT64),
        Register("apparent_energy_export", 3240, 4, ModbusTcpClient.DATATYPE.UINT64),
    ],
    index_shift=-1,
)
