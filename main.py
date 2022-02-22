import logging
import os

from google.cloud import storage

# This application compare the leading bytes of each character in the record
# if they are the same as the UTF-8 bytes.

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Projects/Python/CheckRecordForUtfAndAscii/key.json'

# Create Log file
logging.basicConfig(filename="logfilename.log", level=logging.INFO,
                    format='%(asctime)s,%(msecs)d %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S')


# read file from the bucket
def read_and_verify_the_file():
    """
    This function read all files from a specific bucket or the specific directories from a bucket. These files will be
    checked by the checkFileIfContainsOnlyUTF8Chars() method to make sure it contains non-UTF8 characters.
    :return:
    """
    bucket_name = 'gce-file-test-utf'
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.list_blobs()
    destination_bucket_for_utf8_file = storage_client.get_bucket('record-ready-for-processing')
    destination_bucket_for_bad_char = storage_client.get_bucket('non-utf8-records')
    for file_name in source_blob:
        new_file_name = file_name.name
        print(file_name.name)
        read_output = file_name.download_as_bytes()
        logging.info(f"The file format for {file_name} from the bucket {bucket_name} is readable")
        if checkFileIfContainsOnlyUTF8Chars(read_output):
            # Move the file to record-ready-for-processing bucket
            source_bucket.copy_blob(file_name, destination_bucket_for_utf8_file, new_file_name)
        else:
            # Move the file to non-utf8-records bucket
            source_bucket.copy_blob(file_name, destination_bucket_for_bad_char, new_file_name)


def checkFileIfContainsOnlyUTF8Chars(fileNameBytes):
    # fileNameBytes = read_file(bucket_name)
    """
    This function check if the record has only UTF-8 character.
    :param fileNameBytes:
    :return:
    """
    # Define bad_byte_counter variable for keeping the non UTF 8 characters
    bad_byte_counter = 0
    # Define end variable for keeping the i value and compare later
    end = 0
    # For loop that iterate over the bytes of file
    for i in range(fileNameBytes.__len__()):
        # Octet take each byte value from fileNameBytes
        octet = fileNameBytes[i]
        '''
        # Compare the first Byte using bitwise and-operator(It does an and-operation on each bit position)
        # Example       10010001
        #               10000000
        # That would be 10000000
        '''
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


read_and_verify_the_file()
