import pandas as pd

df = pd.read_csv('desafio.csv')

# esta parte deleta, renomeia, adiciona e ordena as colunas de acordo com o arquivo template_pacientes
df.drop(['RG', 'Telefone', 'Numero do Prontuario', 'Data de Nascimento Responsavel', 'Titular do Plano', 'CPF do Titular do Plano', 'Carteirinha do Plano', 'Observacao', 'Nome do plano', 'Sexo', 'ID', 'Numero Paciente'], axis=1, inplace=True)
df2 = df.rename(columns={'Nome': 'name', 'E-mail': 'email', 'Celular': 'phone', 'CPF':'cpf', 'CEP': 'zipcode', 'Endereco': 'address_1', 'UF': 'state', 'Bairro': 'district', 'Cidade': 'city', 'Responsavel': 'contact_name', 'CPF Responsavel': 'contact_cpf', 'Data de Nascimento': 'birthdate'})
df2['address_2'] = 'N/a'
colunas = ['name', 'email', 'phone', 'birthdate', 'cpf', 'address_1', 'address_2', 'zipcode', 'state', 'city', 'district', 'contact_name', 'contact_cpf']
df2 = df2[colunas]

# regex == simples; função/def == complicado;
# optei pelo uso do regex como meio de validação pela sua simplicidade.
df2['name'] = df2['name'].str.replace(r'^[^.]*\.', '', regex=True)
df2['name'] = df2['name'].str.replace(r'[^\w\s]', '', regex=True)
df2['name'] = df2['name'].str.strip().str.title()

# refatorando email
df2['email'] = df2['email'].str.replace(r'^[\w\.\-]+@[a-z]+\.{2,3}$', '',regex=True)
df2['email'] = df2['email'].str.strip().str.lower()

# refatorando Telefone lambda > função/def;
df2['phone'] = df2['phone'].apply(lambda x:str(x))
df2['phone'] = df2['phone'].apply(lambda x: '('+ x[0:2] + ')' + ' ' + x[2:7] + '-' + x[7:11])

# Refatorando data de aniversário para o padrão do banco de dados
def birthdate(data):
    data_convertida = pd.to_datetime(data)
    data_formatada = data_convertida.strftime('%d/%m/%Y')
    return data_formatada
df2['birthdate'] = df2['birthdate'].apply(birthdate)
print(df2['birthdate'])

# Validação do CPF
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

# Função lambda usando o código de validação para eliminar cpfs inválidos
df2['cpf'] = df2['cpf'].apply(lambda x: x if validate_cpf(str(x)) else 'N/a')

df2 = df2.fillna('')

# padronizando Address_1 & Adress_2 & City & state & district
df2['address_1'] = df2['address_1'].str.strip()
df2['address_2'] = df2['address_2'].str.strip()
#Não suporta str porque todos os valores são nulos NaN
df2['city'] = df2['city'].str.strip()
df2['district'] = df2['district'].str.strip()
df2['state'] = df2['state'].str.strip()

# padronizando contact_name com regex
df2['contact_name'] = df2['contact_name'].str.replace(r'^[^.]*\.', '', regex=True)
df2['contact_name'] = df2['contact_name'].str.replace(r'[^\w\s]', '', regex=True)
df2['contact_name'] = df2['contact_name'].str.strip().str.title()

# Validação do CPF
def validate_cpf(contact_cpf: str) -> bool:
    # Remove qualquer pontuação e mantém apenas os números
    numbers = [int(digit) for digit in contact_cpf if digit.isdigit()]

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

# função lambda usando o código de validação para eliminar cpfs inválidos
df2['contact_cpf'] = df2['contact_cpf'].apply(lambda x: x if validate_cpf(str(x)) else 'N/a')

# padronizando CEP
df2['zipcode'] = df2['zipcode'].str.replace('-', '')

df2 = df2.replace('N/a','')
df2 = df2.replace('NaN', '')
df2 = df2.fillna('')
print(df2)

df2.to_csv('Desafio.csv', index=False)
df2.to_excel('Desafio.xlsx', index=False)