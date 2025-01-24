# Modbus Energy Meter Reader Tool

An example project which shows how you can integrate your software with any energy meter via Modbus protocol.

Easily connect, debug and test any energy meter!

# Installation Guide

## Prerequisites
- `python version 3.9` or later
- `pip` or `uv`

Using pip:
```shell
# Create a Python virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Use requirements.txt to install dependencies
pip install -r requirements.txt

# Then you can run an example reader using following command:
python3 main.py --port 5030 --host localhost
```

Using uv:
```shell
# Create a Python virtual environment
uv venv

# Install dependencies 
uv sync

# Then you can run an example reader using following command:
uv run main.py --port 5030 --host localhost
```


# Integrate your energy meter

## Example:
You can find an example energy meter class inside `energymeter/examples` directory.

In `main.py` you can find an example implementation of polling service that reads the Modbus registers using the specified interval.

```python3
# main.py

from energymeter.examples.example_meter import ExampleMeter  # replace with your custom device class

# Initialize and start the Modbus device
service = ModbusDeviceService(
    host=args.host,
    port=args.port,
    timeout=args.timeout,
    interval=args.interval,
    byteorder=Endian[args.byteorder],
    wordorder=Endian[args.wordorder],
    device=ExampleMeter,
)
service.start_polling()
```

## Writing your own ModbusDevice class:

### Steps:
- Check the manufacturer documentation to find registers you need to read.
- Create the registers map
- Use this map to get the data from the device

```python3
from pymodbus.constants import Endian

from energymeter.device import ModbusDevice
from energymeter.reader import ModbusDeviceDataReader


device = ModbusDevice(
    model="Energy Meter",
    registers_map=[
        Register("value_1", 3000, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_2", 3002, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_3", 3004, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_4", 3200, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_5", 3202, 2, ModbusTcpClient.DATATYPE.INT32),
        Register("value_6", 3204, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_7", 3250, 2, ModbusTcpClient.DATATYPE.UINT64),
        Register("value_8", 3252, 2, ModbusTcpClient.DATATYPE.FLOAT32),
        Register("value_9", 3340, 2, ModbusTcpClient.DATATYPE.FLOAT32),
    ],
    unit=10,
)

client = ModbusTcpClient("192.168.0.1", port=5030, timeout=1)
reader = ModbusDeviceDataReader(
    client=client,
    byteorder=Endian.BIG,
    wordorder=Endian.BIG,
    message_size=100,
    device=device,
)

data = reader.read_registers() # returns a dict with decoded values 

```

## Tests
To run test run following command inside the project directory:

Using native python:
```shell
source .venv/bin/activate
pytest
```

Using uv:
```shell
uv run pytest
```
