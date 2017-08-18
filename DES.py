from collections import deque

PC_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

PC_2 = [14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32]

SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

IP_TABLE = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]

INVERSE_IP_TABLE = [40, 8, 48, 16, 56, 24, 64, 32,
                    39, 7, 47, 15, 55, 23, 63, 31,
                    38, 6, 46, 14, 54, 22, 62, 30,
                    37, 5, 45, 13, 53, 21, 61, 29,
                    36, 4, 44, 12, 52, 20, 60, 28,
                    35, 3, 43, 11, 51, 19, 59, 27,
                    34, 2, 42, 10, 50, 18, 58, 26,
                    33, 1, 41, 9, 49, 17, 57, 25]

E_BIT_SELECTION_TABLE = [32, 1, 2, 3, 4, 5,
                         4, 5, 6, 7, 8, 9,
                         8, 9, 10, 11, 12, 13,
                         12, 13, 14, 15, 16, 17,
                         16, 17, 18, 19, 20, 21,
                         20, 21, 22, 23, 24, 25,
                         24, 25, 26, 27, 28, 29,
                         28, 29, 30, 31, 32, 1]

S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

P_LIST = [16, 7, 20, 21,
          29, 12, 28, 17,
          1, 15, 23, 26,
          5, 18, 31, 10,
          2, 8, 24, 14,
          32, 27, 3, 9,
          19, 13, 30, 6,
          22, 11, 4, 25]


def hex_to_binary(key):
    """Converts a hexadecimal key to its binary representation"""
    counter = 0
    binary_string = ""
    for letter in key:
        counter += 1
        binary_string += bin(int(letter, 16))[2:].zfill(4)
    return list(binary_string)


def permutation(key, values):
    """"Performs a permutation based on values stored in list"""
    permutedkey = []
    for i in range(len(values)):
        permutedkey.insert(i, key[int(values[i]) - 1])
    return permutedkey


def creation_of_16_keys(key):
    """Create the 16 keys for the rounds"""
    # 1. Split the previous permuted key in half
    c_block = key[:len(key) / 2]
    d_block = key[len(key) / 2:]

    # 2. Left shift each half according the SHIFT_TABLE
    # creating each time a pair of blocks
    rotable_c = deque(c_block)
    rotable_d = deque(d_block)

    new_blocks = []
    for i in range(len(SHIFT_TABLE)):
        rotable_c.rotate(-SHIFT_TABLE[i])
        rotable_d.rotate(-SHIFT_TABLE[i])

        c_list = list(rotable_c)
        d_list = list(rotable_d)

        new_block = c_list + d_list

        new_blocks.insert(i, new_block)

    # 3. 48 bits permutation of each key
    new_keys = []
    for i in range(len(new_blocks)):
        new_keys.insert(i, permutation(new_blocks[i], PC_2))

    return new_keys


def encrypt_decrypt(hex_key, plaintext, decryption):
    """Encryption/Decryption"""
    # Key generation
    key = hex_to_binary(hex_key)
    permuted_key = permutation(key, PC_1)
    keys = creation_of_16_keys(permuted_key)

    # Message encode
    binary_message = hex_to_binary(plaintext)

    # Initial permutation
    p_message = permutation(binary_message, IP_TABLE)

    # Feistel (f) function
    l_block = p_message[:len(p_message) / 2]
    r_block = p_message[len(p_message) / 2:]

    l_temp_block = l_block
    r_temp_block = r_block

    for i in range(16):
        new_l_block = r_temp_block
        if not decryption:
            new_r_block = xor_lists(l_temp_block, feistel_function(r_temp_block, keys[i]))
        else:
            new_r_block = xor_lists(l_temp_block, feistel_function(r_temp_block, keys[15 - i]))
        r_temp_block = new_r_block
        l_temp_block = new_l_block

    # Reverse blocks
    reversed_block = list(''.join(r_temp_block) + ''.join(l_temp_block))

    # Final permutation
    final_list = list(list_splitter(permutation(reversed_block, INVERSE_IP_TABLE), 8))

    encoded_message = ""
    for binary_rep in final_list:
        encoded_message += "{:02x}".format(int(''.join(binary_rep), 2), 'x')

    return encoded_message.upper()


def feistel_function(block_32, key):
    """Expansion, key mixing, substitution, permutation"""
    exp_block = permutation(block_32, E_BIT_SELECTION_TABLE)
    xored_list = xor_lists(exp_block, key)

    # Split the list into 6-sized chunks
    new_list = list(list_splitter(xored_list, 6))
    new_list = apply_sbox(new_list)
    # Last permutation
    return permutation(new_list, P_LIST)


def apply_sbox(block_48):
    """Use s-boxes for a new 32-bits block"""
    sboxed_str = ""
    for i in range(len(S_BOXES)):
        # First and last bit
        row_str = block_48[i][0] + block_48[i][5]
        row_int = int(row_str, 2)

        column_str = ''.join(block_48[i][1:5])
        column_int = int(column_str, 2)

        result = S_BOXES[i][row_int][column_int]
        sboxed_str += bin(result)[2:].zfill(4)

    return list(sboxed_str)


def list_splitter(a_list, n):
    """Splits a list into n parts"""
    for i in xrange(0, len(a_list), n):
        yield map(str, a_list[i:i + n])


def xor_lists(list1, list2):
    new_list = []
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            new_list.insert(i, '0')
        else:
            new_list.insert(i, '1')

    return new_list


key = "732061726520736D"
print("1. Encrypt")
print("2. Decrypt")
op = raw_input("Choose an option: ")

if(op=="1"):
    userPlainText = raw_input("Write the PlainText: ")
    data = userPlainText.encode("hex")
    print(data)
    print("CipherText: ")
    print(encrypt_decrypt(key, data, False))
if(op=="2"):
    userPlainText = raw_input("Write the CipherText: ")
    dec = encrypt_decrypt(key, userPlainText, True)
    print(dec)
    datadec = dec.decode("hex")
    print "Decrypted PlainText:", datadec
    
