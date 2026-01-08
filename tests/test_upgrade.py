import json
import pathlib
import pxsol

pxsol.config.current.log = 1

# Load wallet from JSON file
with open("/home/ssszyy/.config/solana/id.json") as f:
    prikey = pxsol.core.PriKey(bytearray(json.load(f)[:32]))
user = pxsol.wallet.Wallet(prikey)

program_pubkey = pxsol.core.PubKey.base58_decode('84Jd3TkNgmw3ibXArJW6DLj3qVATqp7pmeTkpBsVdT8U')
program_data = bytearray(pathlib.Path('target/deploy/pxsol_ss.so').read_bytes())

print(f"User: {user.pubkey.base58()}")
print(f"Program: {program_pubkey.base58()}")
print(f"Program size: {len(program_data)} bytes")
print("\nUpgrading program...")

user.program_update(program_pubkey, program_data)

print("✅ Program upgraded successfully!")
