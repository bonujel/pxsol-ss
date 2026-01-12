import base64
import json
from config import setup_pxsol, PROGRAM_ID, WALLET_PATH

pxsol = setup_pxsol()
pxsol.config.current['log'] = 1

# Load wallet from JSON file
with open(WALLET_PATH) as f:
    prikey = pxsol.core.PriKey(bytearray(json.load(f)[:32]))
user = pxsol.wallet.Wallet(prikey)


def load(user: pxsol.wallet.Wallet) -> bytes:
    prog_pubkey = pxsol.core.PubKey.base58_decode(PROGRAM_ID)
    data_pubkey = prog_pubkey.derive_pda(user.pubkey.p)
    info = pxsol.rpc.get_account_info(data_pubkey.base58(), {})
    return base64.b64decode(info['data'][0])


if __name__ == '__main__':
    print(load(user).decode())  # The quick brown fox jumps over the lazy dog
