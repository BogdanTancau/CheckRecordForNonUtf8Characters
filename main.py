from pathlib import Path

path = Path("C:/Users/a830083/Desktop/DDO/unicod.txt")
# path = Path("C:/Users/a830083/Desktop/DDO/personal_test.txt")
# path = Path("C:/Users/a830083/Desktop/DDO/ascii.txt")
# path = Path("C:/Users/a830083/Desktop/DDO/new_file_test.txt")
# path = Path("C:/Users/a830083/Desktop/DDO/DocsFromMila/TestApp/SCD_personen.txt")

file_from_path = bytearray(open(path, 'rb').read())


def checkFileIfContainsOnlyUTF8Chars(fileNameBytes):
    global char_len
    badCharsCounter = 0
    i = 0
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
        print("true")
        return True
    else:
        print(badCharsCounter, "false")
        return False


checkFileIfContainsOnlyUTF8Chars(file_from_path)
