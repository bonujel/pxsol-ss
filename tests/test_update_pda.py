import base64
import json
import pxsol

pxsol.config.current.log = 1

# Load wallet from JSON file
with open("/home/ssszyy/.config/solana/id.json") as f:
    prikey = pxsol.core.PriKey(bytearray(json.load(f)[:32]))
user = pxsol.wallet.Wallet(prikey)


def save(user: pxsol.wallet.Wallet, data: bytes) -> None:
    prog_pubkey = pxsol.core.PubKey.base58_decode('84Jd3TkNgmw3ibXArJW6DLj3qVATqp7pmeTkpBsVdT8U')
    data_pubkey = prog_pubkey.derive_pda(user.pubkey.p)
    rq = pxsol.core.Requisition(prog_pubkey, [], bytearray())
    rq.account.append(pxsol.core.AccountMeta(user.pubkey, 3))
    rq.account.append(pxsol.core.AccountMeta(data_pubkey, 1))
    rq.account.append(pxsol.core.AccountMeta(pxsol.program.System.pubkey, 0))
    rq.account.append(pxsol.core.AccountMeta(pxsol.program.SysvarRent.pubkey, 0))
    rq.data = bytearray(data)
    tx = pxsol.core.Transaction.requisition_decode(user.pubkey, [rq])
    tx.message.recent_blockhash = pxsol.base58.decode(pxsol.rpc.get_latest_blockhash({})['blockhash'])
    tx.sign([user.prikey])
    txid = pxsol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {})
    pxsol.rpc.wait([txid])
    r = pxsol.rpc.get_transaction(txid, {})
    for e in r['meta']['logMessages']:
        print(e)


def load(user: pxsol.wallet.Wallet) -> bytes:
    prog_pubkey = pxsol.core.PubKey.base58_decode('84Jd3TkNgmw3ibXArJW6DLj3qVATqp7pmeTkpBsVdT8U')
    data_pubkey = prog_pubkey.derive_pda(user.pubkey.p)
    info = pxsol.rpc.get_account_info(data_pubkey.base58(), {})
    return base64.b64decode(info['data'][0])


if __name__ == '__main__':
    save(user, b'The quick brown fox jumps over the lazy dog')
    print(load(user).decode())  # The quick brown fox jumps over the lazy dog
    save(user, '片云天共远, 永夜月同孤.'.encode())
    print(load(user).decode())  # 片云天共远, 永夜月同孤.
