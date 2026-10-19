# INFRAESTRUTURA ABORDADA

Descrição da infraestrutura completa criada para promover a segurança da minha aplicação do azure functions.

## 1. Criação da VNET e subnets
Vamos criar uma VNET e subnets para proteger o banco de dados, expondo-o apenas para conexões dentro da mesma rede virtual.

### Criação da VNET
1. Abrir a tela de criação da VNET
2. COnfigurações usadas:
    - nome: `vnet-melissa`
    - região: `East US 2`
    - Criptografia de rede: `desabilitada`
    - Azure Bastion: `desabilitado`
    - Azure Firewall: `desabilitado`
    - Proteção contra DDoS: `desabilitada`
    - Espaço de endereços da VNet: `10.20.15.0/24`
3. Clicar validar e criar.

### Criação da primeira subnet
Essa primeira subnet vai ser dedicada ao Private Endpoint que vamos estabelecer para o azure storage.
1. Abrir a VNET que criamos `vnet-melissa`
2. Procurar por subnets no menu lateral
3. Clicar em adicionar subnet (+ subnet)

Configurações aplicadas:
- Finalidade: `Default` 
- Nome: `snet-private-endpoints` 
- Intervalo IPv4: `10.20.15.0/24` (intervalo da vnet) 
- Endereço Inicial: `10.20.15.0` 
- Tamanho: `/27` 

> :information_source: O intervalo de `/27` corresponde a 32 endereços (o azure reserva alguns endereços para uso próprio).

- Habilitar a sub-rede privada: `Desabilitada` 
- Gateway de NAT: `Nenhum` 
- Grupo de segurança de rede: `Nenhum` 
- Associação de indetificador de rede: manter valor auto preenchido 
- Delegação de sub rede: `Nenhuma` 
- Política de rede de ponto de extremidade privado: `Desabilitada` 

### Criando o private endpoint para a conta de armazenamento
> :warning: Atenção! O private endpoint é um serviço cobrado por Gb transferido e por hora, ou seja, mesmo sem estar sendo usado, ele é cobrado apenas por existir. Então instancie apenas quando tiver certeza do que está fazendo.

1. Abrir a conta de storage que desejamos proteger
2. Rede > conexões de ponto de extremidade privado
3. Clicar em adicionar private endpoint

Configurações aplicadas:
- assinatura e grupo de recursos: mesmo da vnet
- nome: `pe-tables-melissa`
- região: a mesma da Vnet (muito importante)
- sub recurso de destino: `table`
- rede virtual: `vnet-melissa`
- sub-rede: `snet-private-endpoints`
- configuração de ip privado: `alocação dinâmica`
- Integração com zona DNS privada: `sim`
zona DNS privada: `privatellink.table.core.windows.net` criada automaticamente.

### Integrar o azure functions à Vnet
Para isso vamos criar outra subnet específica para essa integração, que vai servir para criarmos uma rota de saída poara o functions alcançar o endereço privado da Storage Account.
Para isso precisamos confirmar que a região da functions é a mesma da vnet, e o plano é flex consumption.
Configuração da sub rede:
- nome: `snet-functions-integration`
- endereço inicial: `10.20.15.32`
- tamanho: `/27`
- delegar subnet para: `Microsoft.App/environments`
- finalidade: `Default`
- Política de rede de ponto de extremidade privado: `Desabilitada` 

### Conectar o functions à Vnet
1. Abrir o functions
2. Rede > Integração com rede virtual > adicionar integração com Vnet
3. Selecionar a Vnet `vnet-melissa`
4. Selecionar a subnet `snet-functions-integration`
5. Conectar

Neste ponto o functions já consegue se conectar ao endpoint privado do azure tables. Precisamos apenas confirmar que temos um DNS privado vinculado à nossa vnet e apontando para um ip privado pertencente à nossa faixa de rede da vnet privada.

Para essa confirmação vamos:
1. Entrar em **Zonas DNS privadas**
2. Abrir o `privatellink.table.core.windows.net`
3. Entrar em Links de rede virtual
4. Conferir se há o link para `vnet-melissa`
5. Entrar em **Conjuntos de registros**
6. Verificar se já um reigistro com o nome da storage account apontando para um IP privado (esse IP estará dentro da faixa da nossa vnet)


### Verificar se o functions está se comunicando corretamente via conexão privada
Faremos uma chamada do functions para o azure data table mantendo a mesma string de conexão. O DNS deve fazer o direcionamento automático para o ip da subnet, quando a chamada é feita dentro da mesma vnet.

Para confirmar que a chamada chegou via endpoint privado, podemos verificar os logs da conta de armazenamento:
1. Ativar os logs de diagnostico, configurado para enviar para os logs de serviço *Table* para um *Log Analytics workspace*.
2. Procurar nos logs da tabela `StorageTableLogs` o acesso que fizemos, e ver se a propriedade `CallerIpAddress`, que e o IP de origem do acesso, pertence a faixa de ip da nossa subnet.
Podemos usar uma consulta semelhante à:

```kusto
StorageTableLogs
| where TimeGenerated > ago(30m)
| project TimeGenerated, OperationName, StatusCode,
          CallerIpAddress, Uri
| order by TimeGenerated desc
```

### Desativar o acesso público
Finalmente com nossa arquitetura configurada, podemos desativar o acesso público ao recurso:
1. Abra a Storage Account
2. Rede > Acesso à rede pública
3. Selecionar **Desabilitado**
4. Salvar. 

Agora a rede está configurada e os dados da storage table só poderão ser acessados dentro da própria vnet.


## 2. Restringir solicitações para o Azure Functions através do provedor de identidade do entra ID
Essa configuração coloca a chamada aos endpoints do meu functions atrás de um provedor de identidade. Desta forma, temos que fazer login neste provedor de identidade, que nos fornecerá um jwt (JSON Web Token), e o functions só aceitará chamadas com os tokens gerados por este provedor de identidade.
No nosso caso, por coerência com a nossa infraestrutura, colocaremos a aplicação atrás do Microsoft Entra ID.

O processo de autenticação segue o fluxo:
1. O React continua autenticando o usuário pelo MSAL.
2. O React envia um access token destinado à sua API em cada chamada.
3. O Azure Functions valida o token pelo Microsoft Entra ID.
4. Requisições sem token válido são recusadas, mesmo que alguém conheça a URL da Function App.

### Configurando o provedor de identidade
1. Abrir a functions
2. No menu lateral, entrar em autenticação
3. Selecionar *Adicionar provedor de identidade*
4. Escolher **Microsoft** como provedor.
5. Em tipo de locatário, selecionar a configuração de funcionários, usando o tenant corporativo existente.
6. Em registro de aplicativo, selecionar o registro previamente criado no Azure Entra ID (em aplicativos corporativos).
Configurações:
- Requisito de aplicativo cliente: `permitir somente de aplicativos de clientes específicos`
- Aplicativos cliente permitidos: id do app do entra ID
- Exigir autenticação: `Sim`
- Solicitação não autenticadas: `401`

Agora toda chamada sem o token gerado pelo entra ID será bloqueada. A aquisição do token, pra nossa aplicação, ocorrerá no frontend, depois do login bem sucedido, sempre que realizarmos um novo fetch para o banco de dados.

## 0. Criar um aplicativo para gerenciar as identidades Entra ID.

Explicar o processo feito para criação.

Depois colocar um boilerplate de código para conseguir a autenticação no front e depois para conseguir o silentToken do entraID.