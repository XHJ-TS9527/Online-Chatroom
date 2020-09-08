# import modules
import hashlib


def encrypte_password(password_str, salt):
    """
    Parameters
    ----------
    password_str : str
        Password str to be encrypted.
    salt : str
        String of a decimal number.
    Returns
    -------
    encrypted_password : str (length==128)
        Encrypted password string.
    """
    password_str = password_str[::-1]  # 反转
    salt = int(salt * 13)  # 加长盐
    SHA_alg = hashlib.sha512()
    SHA_alg.update(password_str.encode('utf-8'))
    encrypted_password = SHA_alg.hexdigest()  # 第一次加密
    encrypted_password = int('0x' + encrypted_password, 16) + salt  # 加盐
    encrypted_password = hex(encrypted_password)
    MD5_alg = hashlib.md5()
    MD5_alg.update(encrypted_password[2:].encode('utf-8'))  # 第二次加密
    encrypted_password = MD5_alg.hexdigest()
    iteration_alg = (hashlib.md5(), hashlib.sha1(), hashlib.sha256(),
                     hashlib.sha224(), hashlib.sha384())
    for iteration_time in range(10):
        encrypte_alg = iteration_alg[iteration_time % 5]
        if iteration_time % 2:
            encrypted_password = int('0x' + encrypted_password, 16) + salt  # 加盐
            encrypted_password = hex(encrypted_password)
            encrypted_password = encrypted_password[2:]
            salt += 2
        encrypte_alg.update(encrypted_password.encode('utf-8'))
        encrypted_password = encrypte_alg.hexdigest()
    return encrypted_password


def string_plus_plus(string):
    """
    Parameters
    ----------
    string: the string to ++
    Returns
    -------
    string++
    """
    translate_dict = {'0': '1', '1': '2', '2': '3', '3': '4', '4': '5', '5': '6', '6': '7', '7': '8', '8': '9',
                      '9': 'a', 'a': 'b',
                      'b': 'c', 'c': 'd', 'd': 'e', 'e': 'f', 'f': 'g', 'g': 'h', 'h': 'i', 'i': 'j', 'j': 'k',
                      'k': 'l', 'l': 'm',
                      'm': 'n', 'n': 'o', 'o': 'p', 'p': 'q', 'q': 'r', 'r': 's', 's': 't', 't': 'u', 'u': 'v',
                      'v': 'w', 'w': 'x',
                      'x': 'y', 'y': 'z', 'z': 'A', 'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': 'G',
                      'G': 'H', 'H': 'I',
                      'I': 'J', 'J': 'K', 'K': 'L', 'L': 'M', 'M': 'N', 'N': 'O', 'O': 'P', 'P': 'Q', 'Q': 'R',
                      'R': 'S', 'S': 'T',
                      'T': 'U', 'U': 'V', 'V': 'W', 'W': 'X', 'X': 'Y', 'Y': 'Z', 'Z': '0'}
    input_string = list(string)
    input_string.reverse()
    for idx in range(len(input_string)):
        if input_string[idx] == 'Z':
            flag = 1
        else:
            flag = 0
        input_string[idx] = translate_dict[input_string[idx]]
        if not flag:
            break
    input_string.reverse()
    return ''.join(input_string)
