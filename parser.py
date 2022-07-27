from base64 import b64decode, b64encode
from zlib import decompress, compress
import json

#################
#  GLOBAL VARS  #
#################

# list of bits used to encode/decode version numbers
version_bits = [48,32,16,0]

# # dict of compass directions and their associated 'direction' value
# direction_values = {
#     'N': 0,
#     'NE': 1,
#     'E': 2,
#     'SE': 3,
#     'S': 4,
#     'SW': 5,
#     'W': 6,
#     'NW': 7,
# }

# list of compass directions indexed at their associated 'direction' value
direction_values = ['N','NE','E','SE','S','SW','W','NW']

###############
#  FUNCTIONS  #
###############

def bp_string_encode(bp_json):
    """
    Accepts blueprint JSON, encodes, compresses, and returns string.
    """
    # convert JSON to string
    bp_json = json.dumps(bp_json)
    # encode as byte object, compress with zlib level 9, encode with base64, then typecast to string
    bp_string = str(b64encode(compress(bp_json.encode(),9)))
    # strip extra characters, insert leading '0' character, then return
    return '0' + bp_string[2:-1]


def bp_string_decode(bp_string):
    """
    Accepts blueprint string, decodes, uncompresses, and returns JSON.
    """
    # remove first character
    bp_string = bp_string[1:]
    # decode with base64 then decompress with zlib
    bp_string_decoded = decompress(b64decode(bp_string))
    # convert to JSON and return
    return json.loads(bp_string_decoded)

def version_encode(version_num):
    """
    Accepts a version number as string (e.g. '1.1.61'), encodes it for blueprint use,
    and returns as version string (e.g. '281479275675648').
    """
    # split version number at periods into list of ints
    version_list = [int(num) for num in version_num.split('.')]
    # empty int variable to store encoded version
    version_string = 0
    # iterate through version list and shift bits to their respective position
    for i, num in enumerate(version_list):
        version_string += num << version_bits[i]
    # return encoded version typecast back into a string
    return str(version_string)

def version_decode(version_string):
    """
    Accepts a version string (e.g. '281479275675648'), decodes it for readability,
    and returns as version number string (e.g. '1.1.61').
    """
    # convert string to int and declare empty list
    version_string = int(version_string)
    version_list = []
    # iterate through bits, shift appropriately, and append to list
    for bit in version_bits:
        version_list.append(str(version_string >> bit & 0xffff))
    # remove last digit if 0
    version_list.pop(-1) if version_list[-1] == '0' else None
    # return list joined to string
    return '.'.join(version_list)

###############
#  TEST VARS  #
###############

# # belt afk bp from factorio school
# bp_string = '0eNqdm81u2kAUhV8lmjWJPP8z7Lrppo9QRRVJ3NYKGGRMVBTx7jVBqkgUV+ecRaQEMV8+Ljb3zNXwah7Wh3Y3dP1olq/mqd0/Dt1u7La9WZpju785/2wO67HbrVfHdrh53G42h74bu+nxdffc3uwPv1bDuN2Ov83CdI/bfm+W31/NvvvVr9Zn5njctROsG9vN9Ix+tTn/NQ6rfr/bDuPtQ7sezWla2j+1f8zSnhafLH7phvEwPfJv/eUZt1+uVjpq5derlZ5a+e1qZTjdL0zbj2/1eHvdb38cf/SHzUM7TC9n7hUvzG677y6FfjUTqtTmLi7M0Sxvra/pLk7/5akb2sfLc8LZ8QPcEXDLwj0Bdyw8EPDIwiMBTyw8EfDMwjMMrw19tRQCTl8tlYDTV4ttCHql6ZagF5qO36TVepruCTpf90DQ6dvURoIeaHoi6PSNarP4uR4gehHpEaJXgu5Zd9eIdMjdWbFxYO5OpGPuTEcttHsQ6Zh7FDsT5p5EOubOdFX+ei8iHXNn+mpm3X0j0iF3T/RVS7+r3ol0rDJqX8Xcg0jH3KPY+TB3ta9i7sS9aitNJ+5Vx1+RVezaDtoxNSLdQ3QrbiUxuhP3khjdi4kDq7u6VcXoUaRjlUniThijZ3ErjNGLmGewulcxcUD02Ih0qDLRiht5jO7EnTxG92JawuoexDyD0aNIxyqTxBkHRs/ijAOjFzGLYfQq0qF3NTXifAZyT1ZMehjdiXSsMl6cz2DuQcyRGF3NwFhlkphSMTqTgel7NamzpQaiqxnYQuPxRkypkHu2YkrF6E5MqRhdzcBY3dUMjLmrGRhzT2KOxNyzSMfci5gjMXc1A0PupRFTKuRerJhSMboTUypGVzMwVnc1A2PuagbG3JOY9DB6FulYZYqYxTD3KtIh99qIaQlyr1akY+5OzGKYuxcnhpg70VfLVfc4/w7Qib5a6v/o6TN60rIY6J61LAa6Fy1xgHQmAwe2MrZptLEbirdaosFqYxunxQIU77VMgxYnaK0bxTPdNfDFSVrzRvHMjCnxxSnagAzFi1MmsDhWHDOheHHOBBaHOsQUeTwzaUp8cYIWEVB81OY1aHGIu9ZZHk/ctc7xxSliCJk+f06fAquYmfJHX/fpaT1xxITixRnTbDmoI0uB9/ViUpr1DWJ6AX2jmF5mfcWjSahvFuPQrK94HAn1rWJCmfOljiAl2pc5g9RkxNeJKQT09WIKmfUVjxqhvlGMNbO+SUwaoG8Wk8asbxGbP+hbxegy50scI3qfJjBf4hzR+zTx5nu/uHxLaHn1paSFWa8mwPmx4eFm9fN5euSlHfYXh2JDri6HGkOO/nT6CxJT5ss='

# # express belt blueprint book - 1 blueprint each N/S/E/W 2 belts long
# bp_string = '0eNrVlN9ugyAUh9/lXGOj+N9XWRaj9awjs0AAu5rGdx9qlrp0ZSbzxoSbc4Dvd/guuEHddigV46ashfiA4nbvaCheFuW4x46Cz23NTrxqx57pJUIBzOAZCPDqPFZ4lQq19oyquJZCGa/G1sBAgPEGr1AEwysB5IYZhjNxKvqSd+calT3wF4uAFNpeF3ycwiJpGKSHmEAPRZL7h3gYyAOV/o8ajFQ7+PTYYuGGQFvZ+7bXSVtcUOkJQbMgSnOaxoldUXZ/vz8Otye3NPxhgUDDFB7nI9FGphcZ/mOG23sjPvkq88HuzOfPrSQbmQ99V4bbfItvZpV5ujfzYfrcCt3KfObKcJtX7PS+Tn34G8mbvnwClY27YPn9Mzl4wxdOWgs3'

# 1 N express belt
bp_string = '0eNqFj8sKwjAQRf/lrmOxpS/zKyLS6iCBdhKSqbSU/LtJ3bgTZnOHOYc7O8ZpIecNC/QO87AcoK87gnnxMOWdbI6gYYRmKPAw50Sr8xTCSfzAwVkvp5EmQVQw/KQVuow3BWIxYuhrPMJ252UeyaeDfy4FZ0PCLecWSdkWjcKWyHPRxKw/KumfDxTe5MNBVH1Zd5eqa9o0dR/jB0hqTnk='

# 1 N express belt
bp_json = {'blueprint': {'icons': [{'signal': {'type': 'item', 'name': 'express-transport-belt'}, 'index': 1}], 'entities': [{'entity_number': 1, 'name': 'express-transport-belt', 'position': {'x': 6.5, 'y': 10.5}}], 'item': 'blueprint', 'version': 281479275675648}}

version_string = '281479275675648'
version_num = '1.1.61'

#################
#  TEST PRINTS  #
#################

# print(version_encode(version_num))
# print(version_decode(version_string))
# print(bp_string_decode(bp_string))
print(bp_string_encode(bp_json))

# print(bp_string_encode(bp_string_decode(bp_string)))

