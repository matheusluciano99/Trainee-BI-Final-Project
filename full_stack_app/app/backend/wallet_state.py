import reflex as rx

class WalletState(rx.State):
    address: str = ""
    is_connected: bool = False
    
    @staticmethod
    def connect_wallet_js():
        return """
        {   
            if (typeof window.ethereum === 'undefined') {
                alert("MetaMask não encontrada. Verifique se está instalada e habilitada em seu navegador.");
                return;
            }
            
            // Método que dispara o pop-up de conexão
            window.ethereum.request({
                method: 'wallet_requestPermissions',
                params: [{ eth_accounts: {} }]
            })
            .then(() => {
                // Agora que a permissão foi concedida, chamamos 'eth_requestAccounts'
                return window.ethereum.request({ method: 'eth_requestAccounts' });
            })
            .then(accounts => {
                const connectBtn = document.getElementById('connect-wallet');
                const disconnectBtn = document.getElementById('disconnect-wallet');
                const walletSpan = document.getElementById('wallet-address');

                if (accounts && accounts.length > 0) {
                const address = accounts[0];
                if (walletSpan && connectBtn && disconnectBtn) {
                    walletSpan.textContent = address;
                    walletSpan.style.display = 'inline-block';
                    connectBtn.style.display = 'none';
                    disconnectBtn.style.display = 'inline-block';
                    
                    // Salvar localmente (opcional)
                    localStorage.setItem('connectedWallet', address);
                }
                }
            })
            .catch(error => {
                console.error("Erro ao conectar a carteira:", error);
            });
        }"""

    @staticmethod
    def disconnect_wallet_js():
        return """
        {
            if (typeof window.ethereum === 'undefined') {
                alert("MetaMask não encontrada. Verifique se está instalada e habilitada em seu navegador.");
                return;
            }
            window.ethereum.request({
                method: 'eth_requestAccounts',
                params: [{ eth_accounts: {} }]
            })
            .then(() => {
                const walletSpan = document.getElementById('wallet-address');
                if (walletSpan) {
                    walletSpan.textContent = '';
                    walletSpan.style.display = 'none';
                }
                localStorage.removeItem('connectedWallet'); // Remove do localStorage
                document.getElementById('connect-wallet').style.display = 'inline-block'; // Mostra conectar
                document.getElementById('disconnect-wallet').style.display = 'none'; // Esconde desconectar
            })
            .catch(err => {
                console.error("Erro ao desconectar a carteira:", err);
            });
        }"""