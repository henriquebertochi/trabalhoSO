# Simulador de Paginação de Memória

Este projeto implementa um simulador de algoritmos de paginação de memória virtual para sistemas operacionais. O simulador compara o desempenho entre o algoritmo ótimo (teórico) e o algoritmo Segunda Chance em suas variações global e local.

## 📋 Funcionalidades

- **Algoritmo Ótimo**: Implementação do algoritmo teórico que substitui a página que será usada mais distante no futuro
- **Segunda Chance Global**: Todas as páginas competem pelos mesmos quadros de memória usando uma fila circular (clock) com bits de referência
- **Segunda Chance Local**: Divide a memória entre páginas de instruções (I) e dados (D), cada tipo com sua própria fila
- **Modo Didático**: Exibe o estado da memória a cada acesso para fins educacionais
- **Simulação de Interrupções**: Para o algoritmo global, simula interrupções periódicas do SO que zeram os bits de referência

## 🚀 Como Usar

### Sintaxe Básica
```bash
python main.py <arquivo> <tamanho_memoria> [opções]
```

### Parâmetros Obrigatórios
- `<arquivo>`: Arquivo de texto contendo a sequência de acessos às páginas (uma página por linha)
- `<tamanho_memoria>`: Tamanho da memória física (ex: 8MB, 16KB, 1GB)

### Opções Disponíveis
- `--modo-didatico`: Exibe o estado da memória a cada acesso
- `--local`: Usa o algoritmo Segunda Chance Local (padrão é global)
- `--global`: Usa o algoritmo Segunda Chance Global (padrão)
- `--interrupcao N`: Define frequência de interrupções (a cada N acessos) para zerar bits de referência

### Exemplos de Uso

```bash
# Simulação básica
python main.py acessos-pag-Z.txt 200KB

# Com modo didático
python main.py acessos-pag-Z.txt 200KB --modo-didatico

# Usando algoritmo local
python main.py acessos-pag-Z.txt 200KB --local

# Com interrupções a cada 50 acessos
python main.py acessos-pag-Z.txt 200KB --global --interrupcao 50

# Combinando opções
python main.py acessos-pag-Z.txt 200KB --modo-didatico --local
```

## 📁 Estrutura dos Arquivos

### Arquivo de Entrada
O arquivo de entrada deve conter uma página por linha, onde:
- Páginas de instrução começam com 'I' (ex: I0, I1, I2...)
- Páginas de dados começam com 'D' (ex: D0, D1, D2...)

Exemplo do arquivo `acessos-pag-Z.txt`:
```
I0
D0
I0
D1
I0
D2
...
```

## 🔧 Dependências

- Python 3.6+
- pandas

Instale as dependências com:
```bash
pip install pandas
```

## 📊 Saída do Programa

O simulador fornece:

1. **Informações Gerais**:
   - Capacidade da memória em páginas
   - Número de páginas distintas no arquivo

2. **Resultados da Simulação**:
   - Número de faltas de página para cada algoritmo
   - Eficiência do Segunda Chance em relação ao Ótimo

3. **Opcionalmente**:
   - Listagem do número de carregamentos por página
   - Estimativa do tamanho da tabela de páginas

### Exemplo de Saída
```
A memória física comporta 50 páginas.
Há 50 páginas distintas no arquivo.

Com o algoritmo Ótimo ocorrem 100 faltas de página.
Com o algoritmo Segunda Chance ocorrem 150 faltas de página, atingindo 66.67% do desempenho do Ótimo.

Deseja listar o número de carregamentos (s/n)? s
Página   | Carregamentos
D0       | 3
D1       | 3
...

Tamanho estimado da tabela de páginas de 1 nível: 400 bytes
```

## 🧮 Algoritmos Implementados

### Algoritmo Ótimo
- Substitui a página que será referenciada mais distante no futuro
- Serve como referência teórica para comparação
- Não é implementável na prática (requer conhecimento do futuro)

### Segunda Chance Global
- Usa uma fila circular (algoritmo clock)
- Páginas têm bits de referência que são verificados na substituição
- Páginas com bit=1 recebem uma "segunda chance" e têm o bit zerado
- Interrupções periódicas podem zerar todos os bits

### Segunda Chance Local
- Divide a memória igualmente entre instruções e dados
- Cada tipo mantém sua própria fila e bits de referência
- Evita que um tipo de página monopolize a memória

## 💡 Conceitos Educacionais

Este simulador é útil para entender:
- Funcionamento da memória virtual
- Impacto de diferentes estratégias de substituição
- Diferença entre alocação global e local
- Papel dos bits de referência na paginação
- Análise de desempenho de algoritmos de SO

## 🤝 Contribuições

Este é um projeto acadêmico desenvolvido para a disciplina de Sistemas Operacionais. Sugestões e melhorias são bem-vindas!

## 📝 Licença

Projeto desenvolvido para fins educacionais.