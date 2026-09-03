import logging

from fastapi import APIRouter, Depends
from typing import Annotated, Dict, Any

from api.dependencies import db_request, get_current_active_user
from models.request import SQLRequest
from models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()


######################################################
#
# Get relative to all students : /etudiants/[fields]
#
######################################################

@router.get("/etudiants/",
            tags=["student"],
            summary="Students",
            description="Return the list of students")
def get_etudiants(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT 
                            LNM_etudiant.`id_etudiant`,
                            LNM_etudiant.`nom`,
                            LNM_etudiant.`prenom`,
                            LNM_etudiant.`mail`,
                            ExplicitSecondaryKs_LNM_etudiant.ExplicitSecondaryK,
                            ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK as 'promo'
                        FROM LNM_etudiant
                        JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
                        LEFT JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_etudiant.id_promo
                        ORDER BY ExplicitSecondaryK;
                    """,
        "allowedRolesRequester" : ["connected_user"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/etudiants/absences/",
            tags=["student", "administratif"],
            summary="Students",
            description="Return the list of students")
def get_etudiants_absences(
    current_user: Annotated[User, Depends(get_current_active_user)],
    id_responsable: int = -1,
    id_enseignant: int = -1,
):
    request = {
        "request" : f"""SELECT ExplicitSecondaryKs_LNM_etudiant.ExplicitSecondaryK as etudiant, 
                              ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK as promo, 
                              MAQUETTE_module.code_module, 
                              DATE_FORMAT(CLASS_session.schedule, '%Y-%m-%dT%H:%i') AS schedule
                       FROM `CLASS_absence` 
                                JOIN CLASS_session ON CLASS_session.id_session = CLASS_absence.id_session
                                JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
                                JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                                JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                                JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = CLASS_absence.id_etudiant
                                JOIN LNM_promo ON LNM_promo.id_promo = LNM_etudiant.id_promo
                                JOIN LNM_filiere ON LNM_filiere.id_filiere = LNM_promo.id_filiere
                                JOIN LNM_statut ON LNM_statut.id_statut = LNM_promo.id_statut
                                JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
                                JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo
                    """,
        "allowedRolesRequester": ["responsable_etudes"],
    }

    # if id_responsable filter is set
    if id_responsable == current_user.id:
        request["request"] += f""" WHERE MAQUETTE_module.id_responsable = %(id_responsable)s"""
        request["params"] = {
            "id_responsable": id_responsable,
        }
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]

    # if id_enseignant filter is set
    elif id_enseignant == current_user.id:
        request["request"]  += f""" WHERE CLASS_session.id_enseignant = %(id_enseignant)s"""
        request["params"] = {
            "id_enseignant": id_enseignant,
        }
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]

    return db_request(current_user, SQLRequest(**request))


@router.get("/etudiants/stages/",
            tags=["administratif", "student",  "internship",],
            summary="Students",
            description="Return the list of students")
def get_etudiants_stages(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
            SELECT 
                LNM_stage.id_stage,
                LNM_stage.`entreprise`, 
                LNM_stage.`intitulé`, 
                LNM_stage.`description`, 
                LNM_stage.`ville`, 
                DATE_FORMAT(LNM_stage.`date_debut`, '%Y-%m-%d') AS date_debut, 
                DATE_FORMAT(LNM_stage.`date_fin`, '%Y-%m-%d') AS date_fin, 
                LNM_stage.`nature`,
                ExplicitSecondaryKs_LNM_etudiant.ExplicitSecondaryK AS student_fullname,
                LNM_etudiant.mail,
                LNM_etudiant.id_etudiant,
                ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS filiere,
                ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK AS teacher_fullname,
                LNM_enseignant.id_enseignant,
                LNM_enseignant.mail AS teacher_mail,
                CASE
                    WHEN LNM_stage.id_stage IS NULL THEN 'no-internship'
                    WHEN LNM_enseignant.id_enseignant IS NULL THEN 'pending'
                    ELSE 'completed'
                END AS status
            FROM LNM_etudiant
            JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
            JOIN LNM_promo ON LNM_promo.id_promo = LNM_etudiant.id_promo
            JOIN LNM_filiere ON LNM_filiere.id_filiere = LNM_promo.id_filiere
            JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_promo.id_promo
            LEFT JOIN LNM_stage ON LNM_stage.id_etudiant = LNM_etudiant.id_etudiant
            LEFT JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = LNM_stage.id_enseignant
            LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = LNM_enseignant.id_enseignant;
                    """,
        "allowedRolesRequester": ["responsable_etudes", "responsable_stages", "enseignant"],
    }
    return db_request(current_user, SQLRequest(**request))


@router.get("/etudiants/without_stage/",
            tags=["administratif", "student", "internship"],
            summary="Students",
            description="Return the list of students")
def get_etudiants_stages(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
            SELECT `LNM_etudiant`.`id_etudiant`, 
                   `LNM_etudiant`.`nom`,
                   `LNM_etudiant`.`prenom`,
                   ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS "promo"
            FROM `LNM_etudiant` 
                     JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_etudiant.id_promo
            WHERE `LNM_etudiant`.`id_etudiant` 
                      NOT IN ( SELECT `LNM_stage`.`id_etudiant` FROM `LNM_stage` WHERE 1)
                    """,
        "allowedRolesRequester": ["responsable_etudes", "responsable_stages"],
    }
    return db_request(current_user, SQLRequest(**request))


######################################################
#
# Get specific to 1 student : /etudiants/{id_etudiant:int}/[fields]
#
######################################################

@router.get("/etudiants/{id_etudiant:int}",
            tags=["student"],
            summary="Students",
            description="Return the list of students")
def get_etudiant(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
                        SELECT 
                            LNM_etudiant.`id_etudiant`,
                            LNM_etudiant.`nom`,
                            LNM_etudiant.`prenom`,
                            LNM_etudiant.`mail`,
                            LNM_etudiant.`password_updated`,
                            ExplicitSecondaryK,
                            LNM_filiere.nom_filiere,
                            LNM_statut.nom_statut
                        FROM LNM_etudiant
                                 JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
                                 JOIN LNM_promo ON LNM_promo.id_promo = LNM_etudiant.id_promo
                                 JOIN LNM_filiere ON LNM_filiere.id_filiere = LNM_promo.id_filiere
                                 JOIN LNM_statut ON LNM_statut.id_statut=LNM_promo.id_statut
                        WHERE LNM_etudiant.id_etudiant = %(id_etudiant)s;
                    """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester" : ["connected_user"],  # ToDo check allowedRolesRequester
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/etudiants/{id_etudiant:int}/absences/",
            tags=["administratif", "student",],
            summary="Students",
            description="Return the list of students")
def get_etudiant_absences(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request" : """SELECT MAQUETTE_module.code_module, 
                              DATE_FORMAT(CLASS_session.schedule, '%Y-%m-%dT%H:%i') AS schedule
                       FROM `CLASS_absence` 
                                JOIN CLASS_session ON CLASS_session.id_session = CLASS_absence.id_session
                                JOIN MAQUETTE_module_sequence ON MAQUETTE_module_sequence.id_module_sequence = CLASS_session.id_module_sequence
                                JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage
                                JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module
                                JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = CLASS_absence.id_etudiant
                       WHERE LNM_etudiant.`id_etudiant` = %(id_etudiant)s
        """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["responsable_etudes"],
    }
    if current_user.id == id_etudiant:
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))

@router.get("/etudiants/{id_etudiant:int}/load/",
            tags=["student", "administratif", ],
            summary="Students",
            description="Return the list of students")
def get_etudiant_load(
        id_etudiant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request": f"""
                SELECT 
                    DATE_FORMAT(session.schedule, '%Y-%m-%dT%H:%i') AS schedule, 
                    CAST(sequencage.duree_h AS FLOAT) AS duree_h, 
                    module.nom 
                FROM CLASS_session as session 
                    JOIN LNM_groupe as grp ON session.id_groupe = grp.id_groupe 
                    JOIN LNM_promo as promo ON grp.id_promo = promo.id_promo 
                    JOIN LNM_etudiant as etu ON grp.id_promo = etu.id_promo 
                    JOIN MAQUETTE_module_sequence as sequence ON session.id_module_sequence=sequence.id_module_sequence 
                    JOIN MAQUETTE_module_sequencage as sequencage ON sequence.id_module_sequencage=sequencage.id_module_sequencage 
                    JOIN MAQUETTE_module as module ON sequencage.id_module=module.id_module 
                WHERE etu.id_etudiant = %(id_etudiant)s 
            """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["administratif", "enseignant"],
    }
    if current_user.id == id_etudiant:
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))


@router.get("/etudiants/{id_etudiant:int}/edt/",
            tags=["student", "administratif", ],
            summary="Students",
            description="Return the list of students")
def get_etudiant_edt(
        id_etudiant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request": f"""
                    SELECT 
                        etu.nom, 
                        DATE_FORMAT(session.schedule, '%Y-%m-%dT%H:%i') AS date_prevue, 
                        promo.annee, 
                        CAST(sequencage.duree_h AS FLOAT) AS nb_heure, 
                        module.nom AS matiere
                    FROM CLASS_session as session
                        JOIN LNM_groupe as grp ON session.id_groupe = grp.id_groupe
                        JOIN LNM_promo as promo ON grp.id_promo = promo.id_promo
                        JOIN LNM_etudiant as etu ON grp.id_promo = etu.id_promo
                        JOIN MAQUETTE_module_sequence as sequence ON session.id_module_sequence=sequence.id_module_sequence
                        JOIN MAQUETTE_module_sequencage as sequencage ON sequence.id_module_sequencage=sequencage.id_module_sequencage
                        JOIN MAQUETTE_module as module ON sequencage.id_module=module.id_module
                    WHERE etu.id_etudiant =   %(id_etudiant)s
                    ORDER BY session.schedule; 
            """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["administratif",],
    }
    if current_user.id == id_etudiant:
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))


@router.get("/etudiants/{id_etudiant:int}/pastedt/",
            tags=["student",],
            summary="Students",
            description="Return the list of students")
def get_etudiant_pastedt(
        id_etudiant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request": f"""
                    SELECT etu.nom, 
                        DATE_FORMAT(session.schedule, '%Y-%m-%dT%H:%i') AS date_prevue, 
                        promo.annee, 
                        CAST(sequencage.duree_h AS FLOAT) AS nb_heure, 
                        module.nom AS matiere
                    FROM CLASS_session as session
                        JOIN LNM_groupe as grp ON session.id_groupe = grp.id_groupe
                        JOIN LNM_promo as promo ON grp.id_promo = promo.id_promo
                        JOIN LNM_etudiant as etu ON grp.id_promo = etu.id_promo
                        JOIN MAQUETTE_module_sequence as sequence ON session.id_module_sequence=sequence.id_module_sequence
                        JOIN MAQUETTE_module_sequencage as sequencage ON sequence.id_module_sequencage=sequencage.id_module_sequencage
                        JOIN MAQUETTE_module as module ON sequencage.id_module=module.id_module
                    WHERE session.schedule < CURRENT_DATE 
                        AND etu.id_etudiant = %(id_etudiant)s
                    ORDER BY session.schedule; 
            """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["connected_user"],  # ToDo check allowedRolesRequester
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/etudiants/{id_etudiant}/polypoints/",
            tags=["student", ],
            summary="Students",
            description="Return the list of students")
def get_etudiant_pastedt(
        id_etudiant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request": f"""
            SELECT * FROM ETU_polypoint
            WHERE id_etudiant = %(id_etudiant)s
            ORDER BY annee_universitaire DESC; 
            """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["connected_user"],  # ToDo check allowedRolesRequester
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/etudiants/{id_etudiant}/rendus/",
            tags=["student", ],
            summary="Students",
            description="Return the list of students")
def get_etudiant_pastedt(
        id_etudiant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request": f"""
            SELECT rm.description, 
            module.nom, 
            ue.learning_unit_name, 
            rm_etu.avancement,
            rm.date
            FROM LNM_rendu_module as rm 
                JOIN LNM_rendu_module_as_etudiant as rm_etu ON rm_etu.id_rendu_module=rm.id_rendu_module 
                JOIN LNM_etudiant as etu ON etu.id_etudiant=rm_etu.id_etudiant 
                JOIN MAQUETTE_module_as_learning_unit as mue ON rm.id_module=mue.id_module 
                JOIN MAQUETTE_module as module ON mue.id_module=module.id_module 
                JOIN MAQUETTE_learning_unit as ue ON mue.id_learning_unit=ue.id_learning_unit 
            WHERE etu.id_etudiant = %(id_etudiant)s
            """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["connected_user"],  # ToDo check allowedRolesRequester
    }
    return db_request(current_user, SQLRequest(**request))

@router.get("/etudiants/{id_etudiant:int}/stages/",
            tags=["administratif", "student",  "internship",],
            summary="Students",
            description="Return the list of students")
def get_etudiants_stages(
        id_etudiant: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    request = {
        "request" : """
            SELECT LNM_stage.`id_stage`, 
                   ExplicitSecondaryKs_LNM_etudiant.ExplicitSecondaryK AS "étudiant", 
                   ExplicitSecondaryKs_LNM_promo.ExplicitSecondaryK AS "promo", 
                   LNM_stage.`entreprise`, 
                   LNM_stage.`intitulé`, 
                   LNM_stage.`description`, 
                   LNM_stage.`ville`, 
                   DATE_FORMAT(LNM_stage.`date_debut`, '%Y-%m-%d') AS date_debut, 
                   DATE_FORMAT(LNM_stage.`date_fin`, '%Y-%m-%d') AS date_fin, 
                   LNM_stage.`nature`, 
                   ExplicitSecondaryKs_LNM_enseignant.ExplicitSecondaryK AS "enseignant"
            FROM `LNM_stage` 
                     JOIN LNM_etudiant ON LNM_etudiant.id_etudiant = LNM_stage.id_etudiant
                     LEFT JOIN LNM_enseignant ON LNM_enseignant.id_enseignant = LNM_stage.id_enseignant
                     JOIN ExplicitSecondaryKs_LNM_promo ON ExplicitSecondaryKs_LNM_promo.id_promo = LNM_etudiant.id_promo
                     JOIN ExplicitSecondaryKs_LNM_etudiant ON ExplicitSecondaryKs_LNM_etudiant.id_etudiant = LNM_etudiant.id_etudiant
                     LEFT JOIN ExplicitSecondaryKs_LNM_enseignant ON ExplicitSecondaryKs_LNM_enseignant.id_enseignant = LNM_enseignant.id_enseignant
            WHERE LNM_stage.id_etudiant = %(id_etudiant)s;
                    """,
        "params": {
            "id_etudiant": id_etudiant,
        },
        "allowedRolesRequester": ["responsable_etudes", "responsable_stages"],
    }
    if(current_user.id == id_etudiant):
        request["allowedRolesRequester"] += [current_user.ExplicitSecondaryK]
    return db_request(current_user, SQLRequest(**request))

######################################################
#
# Post
#
######################################################

@router.post("/etudiants/{id_etudiant:int}/stage",
            tags=["administratif", "student", "internship",],
            summary="Students",
            description="Return the list of students")
def post_etudiant_stage(
    id_etudiant: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: Dict[str, Any],
):
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    if not 'id_enseignant' in data or not data['id_enseignant']:
        data['id_enseignant'] = 'null'
        request = {
            "request" : """ 
                        INSERT INTO `LNM_stage` (`entreprise`, `intitulé`, `description`, `ville`, `date_debut`, `date_fin`, `nature`, `id_etudiant`) 
                        VALUES (%(entreprise)s, %(intitule)s, %(description)s, %(ville)s, %(date_debut)s, %(date_fin)s, %(nature)s, %(id_etudiant)s)
            """,
        }
    else:
        request = {
            "request" : """ 
                        INSERT INTO `LNM_stage` (`entreprise`, `intitulé`, `description`, `ville`, `date_debut`, `date_fin`, `nature`, `id_etudiant`, `id_enseignant`) 
                        VALUES (%(entreprise)s, %(intitule)s, %(description)s, %(ville)s, %(date_debut)s, %(date_fin)s, %(nature)s, %(id_etudiant)s, %(id_enseignant)s)
            """,
        }
    request.update({
        "params": {
            "entreprise": data['entreprise'],
            "intitule": data['intitule'],
            "description": data['description'],
            "ville": data['ville'],
            "date_debut": data['date_debut'],
            "date_fin": data['date_fin'],
            "nature": data['nature'],
            "id_etudiant": id_etudiant,
            "id_enseignant": data['id_enseignant'],
        },
        "allowedRolesRequester": ["responsable_stages"],
    })
    return db_request(current_user, SQLRequest(**request))


######################################################
#
# Patch
#
######################################################

@router.patch("/etudiants/{id_etudiant:int}/stages/{id_stage:int}",
             tags=["administratif", "student", "internship",],
             summary="Students",
             description="Return the list of students")
def patch_etudiant_stage(
        id_etudiant: int,
        id_stage: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
        data: Dict[str, Any],
):
    # ToDo il pourrait être intéressant de vérifier que le stage est bien à l'étudiant
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request": """
                    UPDATE LNM_stage
                    SET id_enseignant = %(id_enseignant)s
                    WHERE id_stage = %(id_stage)s
        """,
        "params": {
            "id_enseignant": data['id_enseignant'],
            "id_stage": id_stage,
        },
        "allowedRolesRequester": ["responsable_stages"],
    }
    return db_request(current_user, SQLRequest(**request))


######################################################
#
# Delete
#
######################################################

@router.delete("/etudiants/{id_etudiant:int}/stages/{id_stage:int}",
              tags=["administratif", "student", "internship",],
              summary="Students",
              description="Return the list of students")
def delete_etudiant_stage(
        id_etudiant: int,
        id_stage: int,
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    # ToDo il pourrait être intéressant de vérifier que le stage est bien à l'étudiant
    # ToDo convert parameters to be SQLAlchemy Core compatible when it will be up
    request = {
        "request": """
                   DELETE FROM `LNM_stage` WHERE `id_stage`= %(id_stage)s
                   """,
        "params": {
            "id_stage": id_stage,
        },
        "allowedRolesRequester": ["responsable_stages"],
    }
    return db_request(current_user, SQLRequest(**request))



