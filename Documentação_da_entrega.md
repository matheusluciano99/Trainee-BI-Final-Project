# O projeto por enquanto parou no seguinte estado:

Optei por usar o foundry para os contratos, reflex, framework relativamente novo de python, para o frontend e web3.py para fazer a integração com a blockchain. Meu maior problema para o desenvolvimento desse projeto foi a integração do framework reflex com a web3.py e também realizar as chamadas de carteira corretamente, pois para fazer isso foi necessário utilizar um código javascript, cuja linguagem não tenho muito domínio, dentro do reflex para conseguir, por exemplo, pegar a carteira conectada no momento e fazer condições de interação com a condição de estar conectado.

## Pontos feitos:

- Contrato da DAO
- Contrato do Token BCI
- Testes com boa abrangencia.
- Frontend integrado com a blockchain, com chamadas de carteira. O usuário consegue se conectar e desconectar, consegue criar uma proposta, votar nela e executá-la.

## Pontos faltantes:

- O token BCI foi criado, porém não utilizado, pois tive muitos problemas para fazer a integração e comecei testando no anvil com ether mesmo e depois na sepolia também, assim acabei esquecendo de implementar o resto necessário para a utilização do token.

- Limitar o usuário a votar em uma proposta somente 1 vez.

- Implementar um tempo visivel para que a votação na proposta seja encerrada e assim, poder ser executada. No momento, ela pode ser executada a qualquer momento.
