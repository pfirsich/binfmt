#!/usr/bin/env python3
import argparse
import binascii
import struct
from enum import Enum
from dataclasses import dataclass
from typing import Any, Callable


class ByteOrder(Enum):
    Native = "native"
    LittleEndian = "le"
    BigEndian = "be"


byte_order_format = {
    ByteOrder.Native: "@",
    ByteOrder.LittleEndian: "<",
    ByteOrder.BigEndian: ">",
}


@dataclass
class DataType:
    identifier: str
    serializer: str
    constructor: Callable


int_constructor = lambda s: int(s, base=0)


def struct_pack(fmt):
    return lambda val, byte_order: struct.pack(
        f"{byte_order_format[byte_order]}{fmt}", val
    )


copy = lambda s, _: s

data_types = [
    DataType("i8", struct_pack("b"), int_constructor),
    DataType("u8", struct_pack("B"), int_constructor),
    DataType("i16", struct_pack("h"), int_constructor),
    DataType("u16", struct_pack("H"), int_constructor),
    DataType("i32", struct_pack("i"), int_constructor),
    DataType("u32", struct_pack("I"), int_constructor),
    DataType("i64", struct_pack("q"), int_constructor),
    DataType("u64", struct_pack("Q"), int_constructor),
    DataType("f32", struct_pack("f"), float),
    DataType("hex", copy, binascii.unhexlify),
]


@dataclass
class Value:
    byte_order: ByteOrder
    data_type: DataType
    value: Any


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    valid_byte_orders = set(e.name for e in ByteOrder)
    id_type_map = {t.identifier: t for t in data_types}

    for file in args.files:
        current_type = None
        current_byte_order = ByteOrder.Native
        values: list[Value] = []
        with open(file, "r") as f:
            for line in f:
                pre_comment = line.split("#", maxsplit=1)[0]
                parts = pre_comment.split()
                for part in parts:
                    if part in id_type_map:
                        current_type = id_type_map[part]
                    elif part in valid_byte_orders:
                        current_byte_order = ByteOrder(part)
                    else:
                        assert current_type != None
                        print(part)
                        print(current_type.constructor(part))
                        values.append(
                            Value(
                                current_byte_order,
                                current_type,
                                current_type.constructor(part),
                            )
                        )

        outfile = file + ".bin"
        print(outfile)
        with open(outfile, "wb") as f:
            for value in values:
                f.write(value.data_type.serializer(value.value, value.byte_order))


if __name__ == "__main__":
    main()
