# mainnet

def get_abi(name):
    with open(f"abis/{name}.json", 'r') as f:
        return f.read()

compound = dict(
    Comptroller = '0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b',
    cETH = '0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5',
)

aave = dict(
)

dxdy = dict(
)