<footer class="flex flex-col lg:flex-row place-items-center justify-between gap-4 p-4">
    <p class="hidden lg:block">© <?= date("Y") ?> Polytech Annecy Chambery, Inc. All rights reserved.</p>
    <div class="flex justify-center gap-4">
        <!-- Add some other link (Insta ...) -->
        <a href="https://github.com/FlavienVernier/learnagement" target="_blank" class="flex align-center gap-2 h-5">
            <?php include "assets/github-mark.svg"; ?>
        </a>
        <a href="https://www.univ-smb.fr/polytech/formation/informatique-donnees-usages/" target="_blank" class="flex align-center gap-2 h-5">
            <?php include "assets/Logo_Polytech_short.svg"; ?>
        </a>
        <a href="https://www.univ-smb.fr/scem/formations/departement-dinformatique/" target="_blank" class="flex align-center gap-2 h-5">
            <?php include "assets/Logo_Université_Savoie_Mont_Blanc_2015.svg"; ?>
        </a>
    </div>
    <p class="lg:hidden">© <?= date("Y") ?> Polytech Annecy Chambery, Inc. All rights reserved.</p>
</footer>