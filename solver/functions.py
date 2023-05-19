from z3 import Solver, ExprRef, ModelRef, Or, sat

def all_models(s: Solver, *e: ExprRef) -> list[ModelRef]:
    models: list[ModelRef] = []
    s.add(*e)
    while s.check() == sat:
        m = s.model()
        # On stocke le modèle
        models.append(m)
        # On boucle sur tous les éléments auxquels on a donné une interprétation
        # et on retire la possibilité de tomber sur la même valeur pour une même constante
        # par rapport à l'ensemble du modèle
        prevent = [elem() != m[elem] for elem in m.decls() if elem.arity() == 0]
        s.add(Or(*prevent))
    return models