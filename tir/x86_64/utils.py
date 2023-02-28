from elfgenerator.Binary import Binary
def modrm(mod: int, r: int, m: int):
    """Intel Volume 2A 2-6
    
    r changes row
    m changes column
    Not sure which way it's meant to be as long as you're consistent works."""
    mod = mod*2**6
    m = m*2**3
    return mod+r+m


def syscall():
    return Binary(0x050F, 2, 2)