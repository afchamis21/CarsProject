# CarsProject
Software para realizar CRUDs em um banco de dados SQL Server para um pátio de carros.

Feito com Rafael Nascimento (<a href="https://github.com/rsdnrafael">rsdnrafael</a>)

### Techs:
<ul>
  <li>Python</li>
  <li>SQLServer</li>
  <li>PyQt5</li>
  <li>QtDesigner</li>  
</ul>

## As telas do programa:

Tela de login com licença de uso inválida:

![image](https://user-images.githubusercontent.com/92460628/156687620-5134011a-46cb-4feb-910b-1f23c5915b06.png)


Tela de login normal:

![image](https://user-images.githubusercontent.com/92460628/156687746-f5e95b08-c937-4a10-bb09-073dd45f479e.png)


Tela principal, feita para navegação entre as demais telas:

![image](https://user-images.githubusercontent.com/92460628/156687821-3dd2b4ad-ea6c-4b68-9989-3c72b249180a.png)


Tela de adição, nela você pode adicionar carros ao banco de dados, e anexar imagens e documentos ao veículo, que podem ser abertos pelo próprio programa:

![Sem título](https://user-images.githubusercontent.com/92460628/156691168-1b221110-e540-4167-bdc5-5f98fab24f5b.png)


Tela de edição, nela você pode editar os carros que estão no banco de dados. Auto-completa os dados quando o campo de placa do topo é completo. Possui botões especiais para editar as imagens e um pop-up especial para editar os documentos:

![6](https://user-images.githubusercontent.com/92460628/156691595-94348bc6-a1d2-44fe-87c9-e964b207b233.png)


Tela de consulta, nela você pode pesquisar dados no banco, podendo usar todas as colunas como filtro para a pesquisa. Ao selecionar um veículo, os campos de imagem e documentos são completados com os arquivos anexados aos carros. Os documentos são abertos ao clicar duas vezes em seu nome, e as imagens podem ser navegadas pelas setas de navegação. Também se um item estiver selecionado, é possível clicar no lápis para ir direto à tela de edição com os campos já preenchidos. No canto inferior direito, existem mais dois botôes, o de download que gera e baixa um PDF contendo os dados presentes na tabela, e o de e-mail que abre um pop-up do qual é possível enviar e-mails:

![4](https://user-images.githubusercontent.com/92460628/156690950-ec081b92-f7ba-4d1f-bccf-143e97436a59.png)


Pop-up de e-mail, aqui é possível preencher os emails destinatários utilizando ';' como separador, os campos de assunto e mensagem são gerados automaticamente e modificados sempre que os check-box são clicados, é possível também anexar diversos documentos para enviar com o email:

![5](https://user-images.githubusercontent.com/92460628/156692289-b767c2b5-729f-4905-97c4-f1d1f5dff964.png)


A tela de configuração possui duas abas, uma que exibe as informações do usuário logado, e outra com configurações que podem ser customizadas para o prorgama, principalmente sobre as funcionalidades de email:

![2](https://user-images.githubusercontent.com/92460628/156693099-2c2f3835-483d-40a8-ad72-f42eab216f9d.png)


As configurações são: se o pdf gerado deve ser um só com os dados de todos os carros na pesquisa, ou um para cada carro; A mensagem automática de assunto e mensagem exibida no pop-up de email, e informações de login para o email de usuário (necessário para integração com o yagmail, porém senha e e-mail são criptografados no banco de dados)

![3](https://user-images.githubusercontent.com/92460628/156693116-a1efb906-c887-4167-b5b7-5d3fc13afc52.png)


Por último, temos a tela para editar o usuário logado:

![7](https://user-images.githubusercontent.com/92460628/156693518-956514bd-0795-4ff8-9ad7-686db3a93340.png)


