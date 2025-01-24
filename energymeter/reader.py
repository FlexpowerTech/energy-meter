from typing import List

from pymodbus.client.tcp import ModbusTcpClient as MBClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from energymeter.device import ModbusDevice, Register


class RegistersIterator:
    """
    An iterator to implement auto-skip functionality.
    If indices have gaps between each-other skips bytes to read the register correctly.
    """

    def __init__(
        self, registers: List[Register], decoder: BinaryPayloadDecoder
    ):
        self.registers = registers
        self.decoder = decoder
        self.current_register = 0
        self.last_register = len(registers) - 1

        if self.last_register == self.current_register:
            self.current_index = 0
            self.last_index = 0
        else:
            first_register, last_register = registers[0], registers[-1]
            self.current_index = first_register.index
            self.last_index = last_register.index + last_register.length

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= self.last_index:
            raise StopIteration

        register = self.registers[self.current_register]
        if self.current_index != register.index:
            # Skip bytes
            to_skip = register.index - self.current_index
            self.decoder.skip_bytes(to_skip * 2)  # TBD: add to config
            self.current_index = register.index

        value = self.decode_value(register)

        self.current_index = self.current_index + register.length
        self.current_register += 1

        return register, value

    def decode_value(self, register: Register):
        """
        Converts the register to a specific type.
        converter_mapping variable contains supported data types.
        """
        converter_mapping = {
            MBClient.DATATYPE.INT16: "decode_16bit_int",
            MBClient.DATATYPE.UINT16: "decode_16bit_uint",
            MBClient.DATATYPE.INT32: "decode_32bit_int",
            MBClient.DATATYPE.UINT32: "decode_32bit_uint",
            MBClient.DATATYPE.INT64: "decode_64bit_int",
            MBClient.DATATYPE.UINT64: "decode_64bit_uint",
            MBClient.DATATYPE.FLOAT32: "decode_32bit_float",
            MBClient.DATATYPE.FLOAT64: "decode_64bit_float",
        }

        converter_method = converter_mapping.get(register.data_type, None)
        if converter_method is None:
            raise Exception("Not supported data type. Please, implement this.")

        return getattr(self.decoder, converter_method)()


class ModbusDeviceDataReader:
    """
    Modbus RTU over Modbus TCP
    The maximum length of the Message field is is 253 bytes but it
    may differ for specific Modbus devices.
    Check the manufacturer documentation to set a correct value for MAX_MESSAGE_SIZE
    """

    def __init__(
        self,
        client: MBClient,
        device: ModbusDevice,
        byteorder: Endian,
        wordorder: Endian,
        message_size: int,
    ):
        """
        :param client: ModbusTcpClient instance
        :param device: ModbusDevice instance
        :param byteorder: byte endianess. Needed for decoding
        :param wordorder: word endianess. Needed for decoding
        :param max_message_size: Maximum size of register to read per one request
        """
        self.client = client
        self.device = device
        self.byteorder = byteorder
        self.wordorder = wordorder
        self.message_size = message_size

    def break_down_registers_into_chunks(self) -> List[List[Register]]:
        """
        Splits the list of registers to chunks using MAX_MESSAGE_SIZE value
        """
        chunks: List[List[Register]] = []
        registers = self.device.registers

        if len(registers) == 0:
            return chunks

        i, j = 0, 0

        while j < len(registers):
            f, l = registers[i], registers[j]

            if l.index + l.length - f.index > self.message_size:
                chunks.append(registers[i:j])
                i = j
                continue

            if j == len(registers) - 1:
                chunk = registers[i : j + 1]
                if chunk:
                    chunks.append(chunk)

            j += 1

        return chunks

    def read_registers(self):
        """
        Establishs a connection with Modbus device, then reads holding registers,
        decodes the values and store them in a dict data structure.
        """
        data = dict()

        chunks = self.break_down_registers_into_chunks()

        for chunk in chunks:
            first_register, last_register = (
                chunk[0],
                chunk[-1],
            )

            rr = self.client.read_holding_registers(
                first_register.index,
                count=last_register.index
                + last_register.length
                - first_register.index,
                slave=self.device.unit,
            )
            if isinstance(rr, Exception):
                raise rr
            elif rr.function_code >= 0x80:
                raise Exception(
                    f"Can not read registers. function_code: {rr.function_code}"
                )

            decoder = BinaryPayloadDecoder.fromRegisters(
                rr.registers,
                byteorder=self.byteorder,
                wordorder=self.wordorder,
            )

            for register, decoded_value in RegistersIterator(chunk, decoder):
                data[register.name] = decoded_value

        return data
