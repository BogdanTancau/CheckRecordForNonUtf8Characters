# This application compare the leading bytes of each character in the record
# if they are the same as the UTF-8 bytes.

import logging
from pathlib import Path

# Create Log file
logging.basicConfig(filename="logfilename.log", level=logging.INFO,
                    format='%(asctime)s,%(msecs)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S')

# path = Path("C:/Users/a830083/Desktop/DDO/unicod.txt")
# path = Path("C:/Users/a830083/Desktop/DDO/unicod - Copy.txt")
# path = Path("C:/Users/a830083/Desktop/DDO/ascii.txt")
# path = Path("C:/Users/a830083/Desktop/DDO/for_ascii_test.txt")
# path = Path("C:/Users/a830083/Desktop/DDO/file_test.txt")
path = Path("C:/Users/a830083/Desktop/DDO/bad_file_test.txt")

# log from bucket
file_from_path = bytearray(open(path, 'rb').read())


def checkFileIfContainsOnlyUTF8Chars(fileNameBytes):
    # Define bad_byte_counter variable for keeping the non UTF 8 characters
    bad_byte_counter = 0
    # Define end variable for keeping the i value and compare later
    end = 0
    # For loop that iterate over the bytes of file
    for i in range(fileNameBytes.__len__()):
        # Octet take each byte value from fileNameBytes
        octet = fileNameBytes[i]
        # Compare the first Byte using bitwise and-operator(It does an and-operation on each bit position)
        # Example       10010001
        #               10000000
        # That would be 10000000
        if (octet & 0x80) == 0:
            i += 1
            continue  # ASCII
        # Check for UTF-8 leading byte
        if (octet & 0xE0) == 0xC0:
            end = i + 1
        elif (octet & 0xF0) == 0xE0:
            end = i + 2
        elif (octet & 0xF8) == 0xF0:
            end = i + 3
        # Check if i is smaller than end
        while i < end:
            # Increment i
            i += 1
            # Octet take the byte value
            octet = fileNameBytes[i]
            if (octet & 0xC0) != 0x80:
                #  Not a valid trailing byte
                return False
        # Add the number of non UTF 8 Bytes to the bad_byte_counter variable
        bad_byte_counter += 1
    # If bad_byte_counter == 0 the record contains only UTF 8 characters
    if bad_byte_counter == 0:
        # Log message to the Log file
        logging.info('This record can be process')
        return True
    else:
        # If bad_byte_counter != 0 the record contains non UTF 8 characters
        # Log message to the Log file
        logging.error("This record contains bad characters")
        return False


checkFileIfContainsOnlyUTF8Chars(file_from_path)
