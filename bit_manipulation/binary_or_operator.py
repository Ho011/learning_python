
def binary_or(a: int , b: int) -> str:
    """
    Take in 2 integers, convert them to binary,
    return a binary number that is the
    result of a binary or operation on the integers provided.
    """

    if a < 0 or b < 0:
        raise ValueError('The value of both number must be positive')

    a_bin = str(bin(a))[2:] # remove the leading "0b"
    b_bin = str(bin(b))[2:] # remove the leading "0b"

    max_length = max( len(a_bin) , len(b_bin) )

    return '0b' + "".join(
        str( int( '1' in [a_bit , b_bit] ) )
        for a_bit , b_bit in zip(a_bin.zfill(max_length) , b_bin.zfill(max_length))
    )
if __name__ == '__main__':
    print( binary_or(60 , 603) )
    print(60 | 603)
