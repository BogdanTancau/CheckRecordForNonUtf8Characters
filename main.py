import logging
from pathlib import Path

logging.basicConfig(filename="logfilename.log", level=logging.INFO,
                    format='%(asctime)s,%(msecs)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S')

# path = Path("C:/Users/a830083/Desktop/DDO/unicod.txt")
# path = Path("C:/Users/a830083/Desktop/DDO/ascii.txt")
path = Path("C:/Users/a830083/Desktop/DDO/new_file_test.txt")

file_from_path = bytearray(open(path, 'rb').read())


def checkFileIfContainsOnlyUTF8Chars(fileNameBytes):
    global char_len
    badCharsCounter = 0
    end = 0
    for i in range(fileNameBytes.__len__()):
        octet = fileNameBytes[i]
        if (octet & 0x80) == 0:
            i += 1
            continue
        if (octet & 0xE0) == 0xC0:
            end = i + 1
        elif (octet & 0xF0) == 0xE0:
            end = i + 2
        elif (octet & 0xF8) == 0xF0:
            end = i + 3
        while i < end:
            i += 1
            octet = fileNameBytes[i]
            if (octet & 0xC0) < 0x80:
                return False
        badCharsCounter += 1
    if badCharsCounter == 0:
        logging.info('This record can be process')
        return True
    else:
        logging.error(f"This record contains {badCharsCounter} bad characters")
        return False


checkFileIfContainsOnlyUTF8Chars(file_from_path)
