# Modbus Energy Meter Reader Tool

An example project which shows how you can integrate your software with any energy meter via Modbus protocol.

Easily connect, debug and test any energy meter!

# Installation Guide

## Prerequisites
- `python` version 3.9 or later
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

from flexmodbusreader.examples.example_meter import ExampleMeter  # replace with your custom device class

# Initialize and start the Modbus device
service = ModbusDeviceService(
    host=args.host,
    port=args.port,
    timeout=args.timeout,
    interval=args.interval,
    byteorder=Endian.BIG,
    wordorder=Endian.BIG,
    device=ExampleMeter,
)
service.start_polling()
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


## Writing your own ModbusDevice class:

### Steps:
- Check the manufacturer documentation to find registers you need to read.
- Create the registers map
- Use this map to get the data from the device

```python3
from pymodbus.constants import Endian
from pymodbus.client.tcp import ModbusTcpClient

from flexmodbusreader.device import ModbusDevice
from flexmodbusreader.reader import ModbusDeviceDataReader


MyDevice = ModbusDevice(
    model="Energy Meter",
    registers_map=[
      Register("current_phase_a", 3000, 2, ModbusTcpClient.DATATYPE.FLOAT32),
      Register("current_phase_b", 3002, 2, ModbusTcpClient.DATATYPE.FLOAT32),
      Register("current_phase_c", 3004, 2, ModbusTcpClient.DATATYPE.FLOAT32),
      Register("voltage_phase_a", 3028, 2, ModbusTcpClient.DATATYPE.FLOAT32),
      Register("voltage_phase_b", 3030, 2, ModbusTcpClient.DATATYPE.FLOAT32),
      Register("voltage_phase_c", 3032, 2, ModbusTcpClient.DATATYPE.FLOAT32),
      ...
    ],
    unit=10,
)

service = ModbusDeviceService(
    host=args.host,
    port=args.port,
    timeout=args.timeout,
    interval=args.interval,
    byteorder=Endian.BIG,
    wordorder=Endian.BIG,
    device=MyDevice,
)
service.start_polling()
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
