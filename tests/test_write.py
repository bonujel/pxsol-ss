import base64
import json
from config import setup_pxsol, PROGRAM_ID, WALLET_PATH

pxsol = setup_pxsol()
pxsol.config.current['log'] = 1

# Load wallet from JSON file
with open(WALLET_PATH) as f:
    prikey = pxsol.core.PriKey(bytearray(json.load(f)[:32]))
user = pxsol.wallet.Wallet(prikey)


def save(user: pxsol.wallet.Wallet, data: bytes) -> None:
    prog_pubkey = pxsol.core.PubKey.base58_decode(PROGRAM_ID)
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


if __name__ == '__main__':
    save(user, b'The quick brown fox jumps over the lazy dog')
