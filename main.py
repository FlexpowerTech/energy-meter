import argparse
import logging
import time

from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian

from energymeter.device import ModbusDevice
from energymeter.reader import ModbusDeviceDataReader

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class ModbusDeviceService:
    def __init__(
        self,
        host,
        port,
        device: ModbusDevice,
        timeout,
        interval,
        byteorder: Endian,
        wordorder: Endian,
        message_size: int,
    ):
        """
        Initializes the ModbusDevice instance.

        :param host: IP address of the Modbus device
        :param port: Port number of the Modbus device
        :param device: ModbusDevice instance
        :param timeout: Timeout for the Modbus connection
        :param interval: Time interval (in seconds) for data polling
        :param byteorder: byte endianess. Needed for decoding
        :param wordorder: word endianess. Needed for decoding
        :param message_size: Maximum size of register to read per one request
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.interval = interval
        self.device = device
        self.client = ModbusTcpClient(host, port=port, timeout=timeout)
        self.reader = ModbusDeviceDataReader(
            self.client,
            self.device,
            byteorder,
            wordorder,
            message_size,
        )

    def connect(self):
        """Establish a connection to the Modbus device."""
        if self.client.connect():
            logging.info(
                f"Connected to Modbus device at {self.host}:{self.port}"
            )
        else:
            raise ConnectionError(
                f"Failed to connect to {self.host}:{self.port}"
            )

    def disconnect(self):
        """Close the connection to the Modbus device."""
        self.client.close()
        logging.info("Disconnected from Modbus device.")

    def start_polling(self):
        """Continuously poll data at the specified interval."""
        try:
            self.connect()
            while True:
                logging.info("Polling data...")
                data = self.reader.read_registers()
                logging.info(data)
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logging.info("Polling stopped by user.")
        finally:
            self.disconnect()


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

    from energymeter.examples.example_meter import ExampleMeter

    # Initialize and start the Modbus device
    service = ModbusDeviceService(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        interval=args.interval,
        device=ExampleMeter,
        byteorder=Endian[args.byteorder],
        wordorder=Endian[args.wordorder],
        message_size=args.message_size,
    )
    service.start_polling()
