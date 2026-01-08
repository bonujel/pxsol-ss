import base64
import json
import pxsol

pxsol.config.current.log = 1

# Load wallet from JSON file
with open("/home/ssszyy/.config/solana/id.json") as f:
    prikey = pxsol.core.PriKey(bytearray(json.load(f)[:32]))
user = pxsol.wallet.Wallet(prikey)


def load(user: pxsol.wallet.Wallet) -> bytes:
    prog_pubkey = pxsol.core.PubKey.base58_decode('84Jd3TkNgmw3ibXArJW6DLj3qVATqp7pmeTkpBsVdT8U')
    data_pubkey = prog_pubkey.derive_pda(user.pubkey.p)
    info = pxsol.rpc.get_account_info(data_pubkey.base58(), {})
    return base64.b64decode(info['data'][0])


if __name__ == '__main__':
    print(load(user).decode())  # The quick brown fox jumps over the lazy dog
