import reflex as rx

class WalletState(rx.State):
    address: str = ""
    is_connected: bool = False

    @rx.event(background=True)
    async def set_wallet_address(self, address: str):
        async with self:
            self.address = address
            self.is_connected = bool(address)
        yield
        print(f"Saving value {address}")
        print(f"Saving value {self.is_connected}")

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
                    return address;
                }
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