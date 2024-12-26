# Trainee-BI-Final-Project

DAO Voting System

Para rodar o projeto, instale as seguintes dependencias:

- Foundry
- Reflex
- Web3.py
- python-dotenv

Devido a um problema ao compilar o codigo para react usando reflex, realize o procedimento abaixo para rodar o codigo corretamente:

- Rode o comando reflex run. Ao fazer isso acontecerá um erro na pagina.
- Vá para frontend/.web/pages/index.js
- Você verá que tem um erro de sintaxe.
- Substitua esse bloco de codigo por esse abaixo:

const on_click_7c3aa0e9a9cf94580fea387dff3167ef = useCallback(((...args) => (addEvents([(Event("\_call_function", ({ ["function"] : (() => {
if (typeof window.ethereum === 'undefined') {
alert("MetaMask não encontrada. Verifique se está instalada e habilitada em seu navegador.");
return;
}
window.ethereum.request({ method: 'eth_requestAccounts' })
.then(accounts => {
const walletSpan = document.getElementById('wallet-address');
if (walletSpan) {
walletSpan.textContent = accounts[0] || 'Nenhuma conta encontrada';
walletSpan.style.display = 'inline-block';
}
})
.catch(err => {
console.error("Erro ao conectar a carteira:", err);
});
}) }), ({ })))], args, ({ })))), [addEvents, Event])

Assim o app rodará corretamente!
