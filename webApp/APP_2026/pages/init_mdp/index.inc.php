<div id= principal>
    <div id='requete'><h1 id= textprincipal>Initialisation du mot de passe</h1>
    <form action='?page=verification_inscription' method='post'>
    <p>(Utilisateur : <?= $mail ?> )</p>
    <input class=champRecherche type='password' name='mdp1' placeholder='Mot de passe' required><br>
    <input class =champRecherche type='password' name='mdp2' placeholder='Confirmer mot de passe' required><br>
    <input type='hidden' name='id' value='<?= $mail ?>'>
    <input id=bouton type='submit' value='Valider'>
    </div>
</div>