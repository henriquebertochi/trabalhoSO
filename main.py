import sys
import pandas as pd
from collections import defaultdict, deque

TAMANHO_PAGINA = 4096  # 4KB

def converter_memoria(mem_str):
    unidades = {"KB": 2**10, "MB": 2**20, "GB": 2**30}
    for u in unidades:
        if mem_str.upper().endswith(u):
            return int(mem_str[:-len(u)]) * unidades[u]
    raise ValueError("Unidade de memória inválida (ex: 8MB, 16KB, 1GB)")

def ler_acessos(caminho):
    try:
        df = pd.read_csv(caminho, header=None, names=['pagina'])
        return df['pagina'].dropna().astype(str).tolist()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return []

def algoritmo_otimo(acessos, capacidade, modo_didatico=False):
    memoria = set()
    faltas = 0
    futuro = defaultdict(deque)

    for i, pagina in enumerate(acessos):
        futuro[pagina].append(i)

    for i, pagina in enumerate(acessos):
        futuro[pagina].popleft()

        if pagina not in memoria:
            faltas += 1
            if len(memoria) < capacidade:
                memoria.add(pagina)
            else:
                substituir = max(
                    memoria, key=lambda p: futuro[p][0] if futuro[p] else float('inf'))
                memoria.remove(substituir)
                memoria.add(pagina)

        if modo_didatico:
            print(
                f"[ÓTIMO] Acesso {i + 1:>4} → {pagina:<4} | Memória: {sorted(memoria)}")

    return faltas

def segunda_chance_global(acessos, capacidade, modo_didatico=False, interrupcao_freq=0):
    memoria = {}
    ordem = deque()
    referencia = {}
    faltas = 0

    for i, pagina in enumerate(acessos):
        if interrupcao_freq > 0 and (i + 1) % interrupcao_freq == 0:
            ativos = sum(1 for p in referencia if referencia[p] == 1)
            for p in referencia:
                referencia[p] = 0
            if modo_didatico:
                print(f"⚠ Interrupção do SO: Zerando bits de referência das páginas na memória ({ativos} páginas com bit=1)")

        if pagina in memoria:
            referencia[pagina] = 1
        else:
            faltas += 1
            while len(memoria) >= capacidade:
                while True:
                    atual = ordem.popleft()
                    if referencia[atual] == 0:
                        del memoria[atual]
                        break
                    else:
                        referencia[atual] = 0
                        ordem.append(atual)
            memoria[pagina] = True
            referencia[pagina] = 1
            ordem.append(pagina)

        if modo_didatico:
            print(
                f"[2ª CHANCE - GLOBAL] Acesso {i + 1:>4} → {pagina:<4} | Memória: {list(memoria.keys())}")

    return faltas

def segunda_chance_local(acessos, capacidade_total, modo_didatico=False):
    capacidade_instrucao = capacidade_total // 2
    capacidade_dados = capacidade_total - capacidade_instrucao

    mem_instrucao, mem_dados = {}, {}
    ordem_I, ordem_D = deque(), deque()
    ref_I, ref_D = {}, {}

    faltas = 0

    for i, pagina in enumerate(acessos):
        tipo = pagina[0]

        if tipo == 'I':
            memoria, ordem, referencia, capacidade = mem_instrucao, ordem_I, ref_I, capacidade_instrucao
        else:
            memoria, ordem, referencia, capacidade = mem_dados, ordem_D, ref_D, capacidade_dados

        if pagina in memoria:
            referencia[pagina] = 1
        else:
            faltas += 1
            while len(memoria) >= capacidade:
                while True:
                    atual = ordem.popleft()
                    if referencia[atual] == 0:
                        del memoria[atual]
                        break
                    else:
                        referencia[atual] = 0
                        ordem.append(atual)
            memoria[pagina] = True
            referencia[pagina] = 1
            ordem.append(pagina)

        if modo_didatico:
            print(
                f"[2ª CHANCE - LOCAL] Acesso {i + 1:>4} → {pagina:<4} | Instruções: {list(mem_instrucao.keys())} | Dados: {list(mem_dados.keys())}")

    return faltas

def main():
    if len(sys.argv) < 3:
        print(
            "Uso: python trab2.py <arquivo> <tamanho_memoria> [--modo-didatico] [--local|--global] [--interrupcao N]")
        return

    arquivo = sys.argv[1]
    memoria_str = sys.argv[2]
    modo_didatico = '--modo-didatico' in sys.argv
    usar_local = '--local' in sys.argv
    usar_global = '--global' in sys.argv or not usar_local

    interrupcao_freq = 0
    if '--interrupcao' in sys.argv:
        idx = sys.argv.index('--interrupcao')
        if idx + 1 < len(sys.argv):
            try:
                interrupcao_freq = int(sys.argv[idx + 1])
            except:
                print("Erro: valor inválido para --interrupcao.")
                return

    acessos = ler_acessos(arquivo)
    if not acessos:
        print("Arquivo vazio ou mal formatado.")
        return

    paginas_distintas = set(acessos)
    num_distintas = len(paginas_distintas)

    memoria_bytes = converter_memoria(memoria_str)
    capacidade_paginas = memoria_bytes // TAMANHO_PAGINA

    print(f"A memória física comporta {capacidade_paginas} páginas.")
    print(f"Há {num_distintas} páginas distintas no arquivo.")

    faltas_otimo = algoritmo_otimo(acessos, capacidade_paginas, modo_didatico)

    if usar_local:
        faltas_segunda = segunda_chance_local(
            acessos, capacidade_paginas, modo_didatico)
    else:
        faltas_segunda = segunda_chance_global(
            acessos, capacidade_paginas, modo_didatico, interrupcao_freq)

    eficiencia = 100 * faltas_otimo / faltas_segunda if faltas_segunda else 100.0

    print(f"\nCom o algoritmo Ótimo ocorrem {faltas_otimo} faltas de página.")
    print(
        f"Com o algoritmo Segunda Chance ocorrem {faltas_segunda} faltas de página, atingindo {eficiencia:.2f}% do desempenho do Ótimo.")

    listar = input(
        "Deseja listar o número de carregamentos (s/n)? ").strip().lower()
    if listar == 's':
        contagem = defaultdict(int)
        for p in acessos:
            contagem[p] += 1
        print(f"{'Página':<8} | {'Carregamentos'}")
        for p in sorted(paginas_distintas):
            print(f"{p:<8} | {contagem[p]}")

    estimativa = num_distintas * 8  # 8 bytes por entrada (estimativa)
    print(
        f"Tamanho estimado da tabela de páginas de 1 nível: {estimativa} bytes")

if __name__ == "__main__":
    main()
