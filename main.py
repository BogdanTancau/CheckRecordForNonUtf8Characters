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
def read_file():
    bucket_name = 'gce-master-data'
    file_name = ''
    new_bucket_name = 'gce-file-test-utf'
    new_file_name = ''
    # global read_output
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)
    # source_blob = source_bucket.blob(file_name)
    blob_name = source_bucket.list_blobs(prefix='clientData_utf8/SIEMS')
    for file_name in blob_name:
        print(file_name.name)
    # try
        read_output = file_name.download_as_bytes()
        logging.info(f"The file format for {file_name} from the bucket {bucket_name} is readable")
        checkFileIfContainsOnlyUTF8Chars(read_output)
    # return read_output
    # catch

def copy_the_read_file(bucket_name, file_name, new_bucket_name, new_file_name):
    # file_name = ""
    # new_file_name = ""

    """
    Function for moving files between directories or buckets. It will use GCP's copy
    function then delete the blob from the old location.

    inputs
    -----
    bucket_name: name of bucket
    blob_name: str, name of file
        ex. 'data/some_location/file_name'
    new_bucket_name: name of bucket (can be same as original if we're just moving around directories)
    new_blob_name: str, name of file in new directory in target bucket
        ex. 'data/destination/file_name'
    """
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.blob(file_name)
    destination_bucket = storage_client.get_bucket(new_bucket_name)
    blob_name = source_bucket.list_blobs(prefix='clientData_utf8/SIEMS')
    # blob_name = storage_client.list_blobs(bucket_name)
    # for file_name in blob_name:
    #     print(file_name.name)
# new file_name = source_bucket.list_blobs(prefix='clientData_utf8/SIEMS') .copy_blob
    # copy to new destination
    # new_file_name = source_bucket.copy_blob(source_blob.path_helper(blob_name), destination_bucket, new_file_name)
    # new_file_name = source_bucket.copy_blob(
    #     source_blob, destination_bucket, new_file_name)
    # delete in old destination
    # source_blob.delete()

    logging.info(f'File moved from {source_blob} to {new_file_name}')


###############Must search in folder not in bucket
# copy_the_read_file("gce-master-data", "gce-file-test-utf")


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
        # Move the file to ready for processing bucket, and then delete the file from gce-file-test-utf
        copy_the_read_file('gce-file-test-utf', 'ascii_test.txt', 'record-ready-for-processing', 'ascii_test.txt')
        return True
    else:
        # If bad_byte_counter != 0 the record contains non UTF 8 characters
        # Log message to the Log file
        logging.error("This record contains bad characters")
        # Move the file to not_utf8_encoded bucket, and then delete the file from gce-file-test-utf
        copy_the_read_file("gce-file-test-utf", "ascii_test.txt", "non-utf8-records", "ascii_test.txt")
        return False


read_file()

# checkFileIfContainsOnlyUTF8Chars()
