from typing import List, Dict, Tuple

class Automaton:
    def __init__(self, estados, sigma, delta, inicial, final):
        self.estados = estados
        self.sigma = sigma
        self.delta = delta
        self.inicial = inicial  
        self.final = final  

def load_automaton(filename: str) -> Automaton:
    estados = set()
    sigma = set()
    delta = {}
    inicial = None
    final = set()

    with open(filename, 'r') as file:
        lines = file.readlines()

    if len(lines) < 5:
        raise Exception("Formato do arquivo inválido.")

    sigma = set(lines[0].strip().split())
    estados = set(lines[1].strip().split())
    final = set(lines[2].strip().split())
    inicial = lines[3].strip()

    for transition in lines[4:]:
        parts = transition.strip().split()
        if len(parts) != 3:
            raise Exception("Regra de transição inválida.")
        origem, simbolo, destino = parts
        if origem not in estados or destino not in estados or simbolo not in sigma:
            raise Exception("Regra de transição contém símbolos/estados inválidos.")
        if (origem, simbolo) in delta:
            raise Exception("Autômato determinístico requerido.")
        delta[(origem, simbolo)] = destino

    return Automaton(estados, sigma, delta, inicial, final)

def process(automaton: Automaton, words: List[str]) -> Dict[str, str]:
    results = {}
    for word in words:
        current_state = automaton.inicial
        accepted = True
        for symbol in word:
            if symbol not in automaton.sigma:
                results[word] = "INVÁLIDA"
                accepted = False
                break
            current_state = automaton.delta.get((current_state, symbol), None)
            if current_state is None:
                accepted = False
                break
        if accepted and current_state in automaton.final:
            results[word] = "ACEITA"
        else:
            results[word] = "REJEITA"
    return results

def convert_to_nfda(automaton: Automaton) -> Automaton:
    return Automaton(automaton.estados, automaton.sigma, automaton.delta, automaton.inicial, automaton.final)

if __name__ == "__main__":
    try:
        automaton = load_automaton("automaton_description.txt")
        words = ["aba", "abc", "aab", "ba"]
        
        print("Automato carregado com sucesso!")
        
        results = process(automaton, words)
        for word, result in results.items():
            print(f"A palavra '{word}' é {result} pelo autômato.")
        
        nfda_automaton = convert_to_nfda(automaton)
        print("Conversão para NFDA realizada com sucesso!")

    except Exception as e:
        print(f"Erro ao carregar ou processar o autômato: {e}")
