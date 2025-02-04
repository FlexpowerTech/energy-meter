import argparse
import logging

from pymodbus.constants import Endian

from energymeter.service import ModbusDeviceService

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


if __name__ == "__main__":
    # Define command-line arguments
    parser = argparse.ArgumentParser(description="Energy meter Modbus reader")
    parser.add_argument(
        "--host",
        type=str,
        required=True,
        help="IP address of the Modbus device",
    )
    parser.add_argument(
        "--port",
        type=int,
        required=True,
        help="Port number of the Modbus device",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1,
        help="Timeout for the Modbus connection (default: 1 second)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Polling interval in seconds (default: 10 seconds)",
    )
    parser.add_argument(
        "--byteorder",
        type=str,
        choices=["AUTO", "BIG", "LITTLE"],
        default="BIG",
        help="Byte endianess. Default value is 'BIG'.",
    )
    parser.add_argument(
        "--wordorder",
        type=str,
        choices=["AUTO", "BIG", "LITTLE"],
        default="BIG",
        help="Word endianess. Default value is 'BIG'.",
    )
    parser.add_argument(
        "--message_size",
        type=int,
        default=100,
        help="Maximum size of register to read per one request",
    )

    args = parser.parse_args()

    from energymeter.devices.example_meter import ExampleMeter  # replace with your ModbusDevice class

    # Initialize and start the Modbus device
    service = ModbusDeviceService(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        interval=args.interval,
        device=ExampleMeter,  # replace with your ModbusDevice class
        byteorder=Endian[args.byteorder],
        wordorder=Endian[args.wordorder],
        message_size=args.message_size,
    )
    service.start_polling()
