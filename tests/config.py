"""
Network configuration for pxsol-ss tests.

Usage:
    # Default (localhost)
    python tests/test_write.py

    # Use devnet
    SOLANA_NETWORK=devnet python tests/test_write.py
"""
import os

# Network configurations
NETWORKS = {
    'localhost': {
        'rpc_url': 'http://127.0.0.1:8899',
    },
    'devnet': {
        'rpc_url': 'https://api.devnet.solana.com',
    },
}

# Get network from environment variable, default to localhost
NETWORK = os.environ.get('SOLANA_NETWORK', 'localhost')

# Program ID (same across all networks)
PROGRAM_ID = '84Jd3TkNgmw3ibXArJW6DLj3qVATqp7pmeTkpBsVdT8U'

# Wallet path
WALLET_PATH = '/home/ssszyy/.config/solana/id.json'


def get_rpc_url():
    """Get RPC URL for current network."""
    return NETWORKS[NETWORK]['rpc_url']


def setup_pxsol():
    """Configure pxsol to use the selected network."""
    import pxsol
    pxsol.config.current['rpc']['url'] = get_rpc_url()
    return pxsol
