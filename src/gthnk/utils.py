import os
import hashlib


def overwrite_if_different(filename, new_content):
    "Check whether the new_content is different from the existing file."

    # see whether the file exists
    if os.path.isfile(filename):
        # if so, gather the md5 checksums
        with open(filename, "r", encoding='utf-8') as f:
            existing_checksum = hashlib.md5(f.read().encode('utf-8')).hexdigest()
        generated_checksum = hashlib.md5(new_content.encode('utf-8')).hexdigest()

        # compare to md5 checksum of generated file.
        # if different, then overwrite.
        if generated_checksum == existing_checksum:
            return False

    with open(filename, "wb") as f:
        f.write(new_content.encode('utf-8'))
    return True


def overwrite_if_different_bytes(filename, new_content):
    # see whether the file exists
    if os.path.isfile(filename):
        # if so, gather the md5 checksums
        with open(filename, "rb") as f:
            existing_checksum = hashlib.md5(f.read()).hexdigest()
        generated_checksum = hashlib.md5(new_content).hexdigest()

        # compare to md5 checksum of generated file.
        # if different, then overwrite.
        if generated_checksum == existing_checksum:
            return False

    with open(filename, "wb") as f:
        f.write(new_content)
    return True


# create directories
def md(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info("created:\t{0}".format(directory))
    else:
        logging.info("exists:\t{0}".format(directory))


def merge_two_dicts(x, y):
    # go through both loops and make a smart merge
    z = y.copy()
    for day in x:
        for timestamp in x[day]:
            z[day][timestamp] += x[day][timestamp]
    return z


def split_filename_list(filename_str):
    """
    """
    return([x.strip() for x in filename_str.split(',')])
