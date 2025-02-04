# Modbus Energy Meter Reader Tool

An example project which shows how you can integrate your software with any energy meter via Modbus protocol.

Easily connect, debug and test any energy meter!

# Installation Guide

## Prerequisites
- `git`
- `python` version 3.9 or later
- `pip`

Clone or fork the repo first.
```shell
git clone https://github.com/FlexpowerTech/energy-meter.git
```

Navigate to the project directory.
```shell
cd energy-meter
```

Create a virtualenv and install the dependencies.

```shell
# Create a Python virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Use requirements.txt to install dependencies
pip install -r requirements.txt
```

# Integrate your energy meter

Steps:
- Check the manufacturer documentation to find registers you need to read.
- Define the registers map from the registers you need to read.
- Use this map to create a ModbusDevice class

### 1. Define the registers map from the manufacturer documentation
At this stage all you need to do is to determine what indicators you are interested in and write them down, you will use them in the next stage

The manufacturer documentation should contain the list of registers. Choose the register you want to read.

What info do you need:
- Register address;
- Register size;
- Register data type.

**Note:** this example supports following data types:
- INT16 - 16-bit signed integer;
- UINT16 - 16-bit unsigned integer;
- INT32 - 32-bit signed integer;
- UINT32 - 32-bit unsigned integer;
- INT64 - 64-bit signed integer;
- UINT64 - 64-bit unsigned integer;
- FLOAT32 - 32-bit floating-point number;
- FLOAT64 - 64-bit floating-point number.

**Register structure:**
```python3
Register:
    name: str    # Name of the register
    index: int   # Register address
    length: int  # Register size
    data_type: ModbusTcpClient.DATATYPE  # Register data type
```

Once you have identified the list of registers you need, you are ready to move on to the next step. You will use this info to create a ModbusDevice class.


### 2. Create a ModbusDevice class
Create a new python file inside the `energymeter/devices` directory and define a new ModbusDevice class (e.g. my_device.py).

Create a list of registers from the list you have written down at the previous stage and pass it to the ModbusDevice class as a `registers_map` parameter.

```python3
# File: energymeter/devices/my_device.py

from pymodbus.client.tcp import ModbusTcpClient

from flexmodbusreader.device import ModbusDevice, Register
from flexmodbusreader.reader import ModbusDeviceDataReader


MyDevice = ModbusDevice(
    model="My Own Meter",  # Name of the device
    registers_map=[        # List of registers to read
      Register("current_phase_a", 3000, 2, ModbusTcpClient.DATATYPE.FLOAT32),
      Register("current_phase_b", 3002, 2, ModbusTcpClient.DATATYPE.FLOAT32),
      Register("current_phase_c", 3004, 2, ModbusTcpClient.DATATYPE.FLOAT32),
      ...
    ]
)
```

### 3. Use your new device class in the main script

In `main.py` you can find an example implementation of polling service that reads the Modbus registers using the specified interval.

The service simply reads the data from the energy meter and prints it to the console.

```python3
# File: main.py

from energymeter.devices.my_device import MyDevice  # import your device class

# Initialize and start the Modbus device
service = ModbusDeviceService(
    host=args.host,
    port=args.port,
    timeout=args.timeout,
    interval=args.interval,
    byteorder=Endian.BIG,
    wordorder=Endian.BIG,
    device=MyDevice,  # Pass your device class here
)
service.start_polling()
```

### 4. Run the service
Connect your device to the network and run the service using the following command:
```
python main.py --host {IP_ADDRESS} --port {PORT}
```

Script arguments:
```shell
python main.py --help
usage: main.py [-h] --host HOST --port PORT [--timeout TIMEOUT] [--interval INTERVAL] [--byteorder {AUTO,BIG,LITTLE}] [--wordorder {AUTO,BIG,LITTLE}] [--message_size MESSAGE_SIZE]

Energy meter Modbus reader

options:
  -h, --help            show this help message and exit
  --host HOST           IP address of the Modbus device
  --port PORT           Port number of the Modbus device
  --timeout TIMEOUT     Timeout for the Modbus connection (default: 1 second)
  --interval INTERVAL   Polling interval in seconds (default: 10 seconds)
  --byteorder {AUTO,BIG,LITTLE}
                        Byte endianess. Default value is 'BIG'.
  --wordorder {AUTO,BIG,LITTLE}
                        Word endianess. Default value is 'BIG'.
  --message_size MESSAGE_SIZE
                        Maximum size of register to read per one request
```


## Examples:
You can find an example energy meter class inside `energymeter.devices.example_meter` module.

```python3
# File: energymeter/examples/example_meter.py

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

```

## Tests
To run test run following command inside the project directory:

Using native python:
```shell
source .venv/bin/activate
pytest
```
