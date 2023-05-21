from z3 import Solver, ExprRef, ModelRef, Or, sat, unsat

def all_models(s: Solver, *e: ExprRef, max_models: int | None = None) -> list[ModelRef]:
    models: list[ModelRef] = []
    s.add(*e)
    def collect_model(s: Solver, mdls: list[ModelRef]):
        m = s.model()
        # print(m, "\n")
        # On stocke le modèle
        mdls.append(m)
        # On boucle sur tous les éléments auxquels on a donné une interprétation
        # et on retire la possibilité de tomber sur la même valeur pour une même constante
        # par rapport à l'ensemble du modèle
        prevent = [elem() != m[elem] for elem in m.decls() if elem.arity() == 0]
        s.add(Or(*prevent))
    if max_models:
        for _ in range(max_models):
            if s.check() == unsat:
                return models
            collect_model(s, models)
    else: 
        while s.check() == sat:
            collect_model(s, models)
    return models