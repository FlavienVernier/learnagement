# Permissions

## Structural role

- Administratif :
- Enseignant :
- Étudiant :

Un utilisateur est forcément dans l'un, et un seul, de ces rôles.  

## Institutional role

La définition des rôles institutionnels est libre. Chaque rôle institutionnel peut être associé à 1 ou plusieurs utilisateurs, quelque soit son rôle structurel. 

## Advanced permission system

Permet de définir un mécanisme de rôles et responsabilités plus complex basé sur une logique de 1e ordre.

Exemple :

| Rôle utilisateur                    | Scope demandé                         | Résultat          |
|-------------------------------------|---------------------------------------|-------------------|
| `{}`                                | n'importe quoi                        | ✅ wildcard total  |
| `{"filiere":"IDU"}`                 | `{"filiere":"IDU","niveau":"FI4"}`    | ✅ filière couvre  |
| `{"filiere":"IDU","niveau":"FI4"}`  | `{"filiere":"IDU","niveau":"FI4"}`    | ✅ exact           |
| `{"filiere":"IDU","niveau":"FI4"}`  | `{"filiere":"IDU"}`                   | ❌ trop précis     |
| `{"filiere":"SEA"}`                 | `{"filiere":"IDU","niveau":"FI4"}`    | ❌ mauvaise valeur |
| `{"filiere":"IDU","semestre":"S8"}` | `{"filiere":"IDU","niveau":"FI4"}`    | ❌ dimension diff  |



requests = {

    "get_semestre_etudiants": {
        "request": "SELECT * FROM inscriptions WHERE filiere = %(filiere) AND semestre = %(semestre)",
        "params": lambda filiere, semestre: {"filiere": filiere, "semestre": semestre},
        "allowedRolesRequester": lambda params, user: (
            True if has_responsabilite(user, "semestre", {
                "filiere":  params.get("filiere"),
                "semestre": params.get("semestre"),
            })
            else ["administratif"]
        ),
    },
}