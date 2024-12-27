# Trainee-BI-Final-Project

DAO Voting System

Para rodar o projeto, instale as seguintes dependencias:

- Foundry
- Reflex
- Web3.py
- python-dotenv

Devido a um problema ao compilar o codigo para react usando reflex, realize o procedimento abaixo para rodar o codigo corretamente:

- Rode o comando "reflex run". Ao fazer isso acontecerá um erro na pagina.
- Vá para frontend/.web/pages/index.js
- Você verá que tem um erro de sintaxe.
- Substitua esses blocos de codigo como indicado abaixo:

  - a partir da linha 91, substitua o codigo da função por esse:

  const on_click_f5dbb94f265300f754219fd02a635921 = useCallback(((...args) => (addEvents([(Event("\_call_function", ({ ["function"] : (() => {
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
        }) }), ({  })))], args, ({  })))), [addEvents, Event])

  - a partir da linha 143, substitua o codigo da função por esse:

  export function Button_6640db8d3eb4c73c4a2227a56595278b () {
  const ref_disconnect_wallet = useRef(null); refs["ref_disconnect_wallet"] = ref_disconnect_wallet;
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_click_eab1431134ec68d01707c9c5e35c18e8 = useCallback(((...args) => (addEvents([(Event("\_call_function", ({ ["function"] : (() => {
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
  }) }), ({ })))], args, ({ })))), [addEvents, Event])

Assim o app rodará corretamente!
