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