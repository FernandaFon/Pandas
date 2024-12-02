Um de nossos clientes, uma grande rede de clínicas de saúde, solicitou nossa ajuda para migrar os dados de pacientes de um sistema antigo para o novo sistema que desenvolvemos. Esses dados chegaram até nós em um arquivo CSV cheio de inconsistências e erros comuns, como campos em branco, formatos incorretos e informações mal formatadas.

**Sua missão:**

1. **Ler e entender o arquivo CSV sujo** fornecido.
2. **Aplicar as regras de tratamento necessárias** para preparar os dados de acordo com as especificações do banco de dados, use o Python para isso.
3. **Salvar o resultado** em um arquivo CSV pronto para o carregamento.

### **Regras do Banco de Dados**

Você deve garantir que o arquivo final siga estas regras:

- **`name`**: Campo obrigatório! Os nomes devem ser padronizados no formato Título (ex.: "João da Silva"). Dica: use o método `.title()` para isso.
- **`email`**: Apenas e-mails válidos que contenham os **domínios** (Exemplo: *@servico.com* ou *@servico.com.br)*. Não deve haver espaços ou caracteres especiais inválidos.
- **`phone`**: Garantir que os números estejam no formato (XX) XXXXX-XXXX. O DDD é obrigatório.
- **`birthdate`**: Datas devem estar no formato DD/MM/AAAA.
- **`cpf`**: Validar os CPFs usando a função fornecida.
- `address_1`: Precisa ser `string`
- `address_2`: Precisa ser `string`
- `zipcode`: Garantir que os números estejam no formato XXXXXXXX.
- `state` : Precisa ser `string`
- `city` : Precisa ser `string`
- `district` : Precisa ser `string`
- `contact_name`: Os nomes devem ser padronizados no formato Título (ex.: "João da Silva"). Dica: use o método `.title()` para isso.
- `contact_cpf`: Validar os CPFs usando a função fornecida

**Essas são as regras principais que não podem ser negligenciadas.**

### **O que esperamos no resultado final**

Um arquivo CSV limpo, pronto para ser carregado no banco de dados, com todos os campos no formato correto e sem erros e o código **python** utilizado para a limpeza.

Função para a validação do CPF

def validate_cpf(cpf: str) -> bool:
    # Remove qualquer pontuação e mantém apenas os números
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True
