import argparse
import os
from graphs.io import process_bairros_data

def main():
    """
    Ponto de entrada principal para a interface de linha de comando.
    """
    parser = argparse.ArgumentParser(description="Análise de Grafos do Recife")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando para processar os nós (bairros)
    parser_process = subparsers.add_parser("process-nodes", help="Processa o CSV de bairros para criar a lista de nós.")
    parser_process.set_defaults(func=handle_process_nodes)

    args = parser.parse_args()
    args.func(args)

def handle_process_nodes(args):
    """
    Lida com o comando 'process-nodes', executando a limpeza e transformação dos dados.
    """
    # Define os caminhos baseados na estrutura de pastas do projeto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'data', 'bairros_recife.csv')
    output_path = os.path.join(base_dir, 'data', 'bairros_unique.csv')
    
    print(f"Lendo dados de: {input_path}")
    
    try:
        process_bairros_data(input_path, output_path)
        print(f"Processamento concluído. Nós salvos em: {output_path}")
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada não encontrado em '{input_path}'.")
        print("Certifique-se que o arquivo 'bairros_recife.csv' está na pasta 'data/'.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()