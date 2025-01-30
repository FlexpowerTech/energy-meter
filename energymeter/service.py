import logging
import time

from flexmodbusreader.device import ModbusDevice
from flexmodbusreader.reader import ModbusDeviceDataReader
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian


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
