import reflex as rx

class WalletState(rx.State):
    address: str = ""
    is_connected: bool = False
    
    def set_address(self, address: str):
        self.address = address
        self.is_connected = bool(address)

    async def handle_wallet_connection(self):
        """Handle wallet connection events from JS"""
        return rx.run_script("""
            window.addEventListener('walletConnected', (event) => {
                setState('address', event.detail.address);
            });
        """)

    @staticmethod
    def connect_wallet_js():
        return """{
        async function connectWallet() {
            try {
                if (typeof window.ethereum === 'undefined') {
                    alert("MetaMask not found");
                    return;
                }
                
                await window.ethereum.request({
                    method: 'wallet_requestPermissions',
                    params: [{ eth_accounts: {} }]
                });
                
                const accounts = await window.ethereum.request({
                    method: 'eth_requestAccounts'
                });
                
                if (accounts && accounts.length > 0) {
                    const address = accounts[0];
                    document.getElementById('wallet-address').textContent = address;
                    document.getElementById('wallet-address').style.display = 'inline-block';
                    document.getElementById('connect-wallet').style.display = 'none';
                    document.getElementById('disconnect-wallet').style.display = 'inline-block';
                    
                    window.dispatchEvent(new CustomEvent('walletConnected', {
                        detail: { address: address }
                    }));
                    
                    localStorage.setItem('connectedWallet', address);
                }
                
                window.ethereum.on('accountsChanged', function(accounts) {
                    if (accounts.length > 0) {
                        window.dispatchEvent(new CustomEvent('walletConnected', {
                            detail: { address: accounts[0] }
                        }));
                    }
                });
            } catch (err) {
                console.error("Connection error:", err);
                alert(err.message);
            }
        }
        connectWallet();}
        """

    @staticmethod
    def disconnect_wallet_js():
        return """{
        async function disconnectWallet() {
            try {
                document.getElementById('wallet-address').textContent = '';
                document.getElementById('wallet-address').style.display = 'none';
                document.getElementById('connect-wallet').style.display = 'inline-block';
                document.getElementById('disconnect-wallet').style.display = 'none';
                localStorage.removeItem('connectedWallet');
                
                window.dispatchEvent(new CustomEvent('walletConnected', {
                    detail: { address: '' }
                }));
            } catch (err) {
                console.error("Disconnection error:", err);
                alert(err.message);
            }
        }
        disconnectWallet();}
        """