<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Dashboard — Learnagement<?php $t->endSlot(); ?>

<?= $t->startSlot('stylesheet') ?>
    <link rel="stylesheet" href="https://uicdn.toast.com/calendar/latest/toastui-calendar.min.css" />
<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>
    <?php
        $type = $user['type'];
        $id_etudiant = $type === 'etudiant' ? $user['id'] : null;
        $id_enseignant = $type === 'enseignant' ? $user['id'] : null;
        $id_administratif = $type === 'administratif' ? $user['id'] : null;

        $sql = "SELECT * FROM `LNM_calendar` WHERE 
                (id_etudiant = ? OR (? IS NULL AND id_etudiant IS NULL)) AND
                (id_enseignant = ? OR (? IS NULL AND id_enseignant IS NULL)) AND
                (id_administratif = ? OR (? IS NULL AND id_administratif IS NULL))";
        $stmt = mysqli_prepare($pdo, $sql);
        mysqli_stmt_bind_param($stmt, "iiiiii", $id_etudiant, $id_etudiant, $id_enseignant, $id_enseignant, $id_administratif, $id_administratif);
        mysqli_stmt_execute($stmt);
        $result = mysqli_stmt_get_result($stmt);
    ?>
    <?php
        $heure   = (int) date('H');
        $salut   = match(true) {
            $heure < 12 => 'Bonjour',
            $heure < 18 => 'Bon après-midi',
            default     => 'Bonsoir',
        };
    ?>

    <section class="flex-1 flex flex-col gap-4">
        <!-- En-tête -->
        <div class="flex items-center justify-between mb-4">
            <div>
                <p class="text-xs text-slate-400 mb-0.5"><?= date('l j F Y') ?></p>
                <h1 class="text-2xl font-medium text-[#0f2744]">
                    <?= $salut ?>, <?= htmlspecialchars($user['email']) ?> 👋
                </h1>
            </div>
        </div>
        <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <?php if ($user['type'] !== 'administratif') : ?>
                <a href="<?= ($user['type'] === 'etudiant') ? $t->router->href("dashboard-rendus-student") : $t->router->href("dashboard-rendus-enseignant") ?>" class="bg-white rounded-xl shadow p-4 hover:shadow-md transition space-y-2">
                    <h2 class="text-xl font-semibold text-blue-700">
                        📄 Rendus à venir
                    </h2>
                    <p class="text-gray-600">
                        Consultez vos devoirs à rendre et leurs échéances.
                    </p>
                </a>
            <?php endif; ?>

            <?php if ($user['type'] === 'etudiant') : ?>
                <a href="<?= $t->router->href("dashboard-profile") ?>"
                class="bg-white rounded-xl shadow p-4 hover:shadow-md transition space-y-2">
                    <h2 class="text-xl font-semibold text-green-700">
                        ⭐ Polypoints
                    </h2>
                    <p class="text-gray-600">
                        Suivez vos engagements et points acquis.
                    </p>
                </a>
            <?php endif; ?>

            <a href="<?= $t->router->href("dashboard-ressource") ?>"
            class="bg-white rounded-xl shadow p-4 hover:shadow-md transition space-y-2">
                <h2 class="text-xl font-semibold text-purple-700">
                    📚 Ressources
                </h2>
                <p class="text-gray-600">
                    Accédez aux services et outils universitaires.
                </p>
            </a>
        </section>

        <section class="grid grid-cols-1 gap-6 grow">
            <div class="lg:col-span-2 bg-white rounded-xl shadow p-6 space-y-4 flex flex-col">
                <div class="bg-white border border-black/8 rounded-xl px-4 py-3 flex flex-col md:flex-row items-center justify-between gap-3 mb-4">
                    <!-- Navigation -->
                    <div class="flex items-center gap-1">
                        <button id="prevbtn"
                                class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-500 hover:bg-slate-100 hover:text-[#0f2744] transition-colors">
                            <svg width="15" height="15" fill="none" viewBox="0 0 24 24">
                                <polyline points="15 18 9 12 15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <button id="todaybtn"
                                class="h-8 px-3 text-xs font-medium text-slate-600 hover:bg-slate-100 hover:text-[#0f2744] rounded-lg transition-colors">
                            Aujourd'hui
                        </button>
                        <button id="nextbtn"
                                class="w-8 h-8 flex items-center justify-center rounded-lg text-slate-500 hover:bg-slate-100 hover:text-[#0f2744] transition-colors">
                            <svg width="15" height="15" fill="none" viewBox="0 0 24 24">
                                <polyline points="9 18 15 12 9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>

                    <!-- Titre de la période courante -->
                    <span id="calendar-title" class="text-sm font-medium text-[#0f2744] flex-1 text-center"></span>

                    <!-- Input lien + submit -->
                    <div class="flex items-center gap-2">
                        <form method="POST" action="<?= $t->router->href('profile-calendar') ?>"
                            class="flex items-center gap-0 rounded-lg overflow-hidden border border-slate-200 bg-white focus-within:ring-2 focus-within:ring-[#0f2744] focus-within:border-transparent transition-all">
                            <input type="hidden" name="hasAgenda" value="<?= mysqli_num_rows($result) > 0 ?>">
                            <div class="flex items-center pl-2.5 text-slate-400">
                                <svg width="14" height="14" fill="none" viewBox="0 0 24 24">
                                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"
                                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"
                                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </div>
                            <input id="calendar-link-input"
                                type="url"
                                name="url"
                                placeholder="Coller un lien..."
                                class="h-8 pl-2 pr-2 text-xs text-slate-700 placeholder-slate-400 bg-transparent outline-none w-48 border-0" />
                            <button id="calendar-link-submit" type="submit"
                                    class="h-8 px-3 text-xs font-medium text-white bg-[#0f2744] hover:bg-[#1a3a6b] transition-colors">
                                Ajouter
                            </button>
                        </form>
                    </div>
                        
                    <!-- Sélecteur de vue -->
                    <div class="flex items-center gap-1 bg-slate-100 rounded-lg p-0.5">
                        <button data-view="day"
                                class="view-btn h-7 px-3 text-xs font-medium rounded-md text-slate-500 hover:text-[#0f2744] transition-colors">
                            Jour
                        </button>
                        <button data-view="week"
                                class="view-btn h-7 px-3 text-xs font-medium rounded-md text-slate-500 hover:text-[#0f2744] transition-colors">
                            Semaine
                        </button>
                        <button data-view="month"
                                class="view-btn h-7 px-3 text-xs font-medium rounded-md text-slate-500 hover:text-[#0f2744] transition-colors">
                            Mois
                        </button>
                    </div>
                </div>
                <div id="calendar" class="flex-1"></div>
            </div>
        </section>
    </section>
</div>
<?php $t->endSlot(); ?>

<?= $t->startSlot('script.top') ?>
    <script src="https://uicdn.toast.com/calendar/latest/toastui-calendar.min.js"></script>
<?php $t->endSlot(); ?>

<?= $t->startSlot('script.bottom') ?>
    <script>
        const urls = [
            <?php foreach($result as $agenda) : ?>
                "<?= $agenda['url'] ?>"
            <?php endforeach; ?>
        ]    
        // TODO: CHANGER LE LIEN
        const Calendar = tui.Calendar;
        const calendar = new Calendar('#calendar', {
            defaultView: 'week',
            week: {
                startDayOfWeek: 1,
                dayNames: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
                taskView: false,
                eventView: ['time'],
            },
            month: {
                startDayOfWeek: 1,
                dayNames: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
            },
            useFormPopup: false,
            useDetailPopup: true,
            template: {
                time(event) {
                    return `
                        <div style="color: white;">
                            <strong>${event.title}</strong><br/>
                            ${event.location ? `📍 ${event.location}<br/>` : ''}
                            ${event.body ? `<small>${event.body}</small>` : ''}
                        </div>
                    `;
                }
            }
        });

        document.getElementById('nextbtn').addEventListener('click', () => {
            calendar.next();
        });
        document.getElementById('prevbtn').addEventListener('click', () => {
            calendar.prev();
        });
        document.getElementById('todaybtn').addEventListener('click', () => {
            calendar.today();
        });
        document.querySelectorAll('button[data-view]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const view = e.target.dataset.view;
                calendar.changeView(view, true);
            });
        });

        urls.forEach(url => {
            fetch(`https://corsproxy.io/?${encodeURIComponent(url)}`)
                .then(response => response.text())
                .then(data => {
                    const rawEvents = data.match(/BEGIN:VEVENT[\s\S]*?END:VEVENT/g);
                    const events = rawEvents.map(block => {
                        const dtstart = block.match(/^DTSTART[^:]*:(.+)/m)?.[1].trim();
                        const dtend = block.match(/^DTEND[^:]*:(.+)/m)?.[1].trim();
                        const summary = block.match(/^SUMMARY:(.+)/m)?.[1].trim();
                        const location = block.match(/^LOCATION:(.+)/m)?.[1].trim();
    
                        const unfolded = block.replace(/\r?\n[ \t]/g, '');
                        const description = unfolded.match(/^DESCRIPTION:(.+)/m)?.[1].trim()
                            ?.replace(/\\n/g, '\n')   // sauts de ligne
                            ?.replace(/\\,/g, ',')    // virgules
                            ?.replace(/\\;/g, ';')    // points-virgules
                            ?.replace(/\\\\/g, '\\'); // backslash
    
                        const formatDate = (str) => {
                            return new Date(
                                str.replace(
                                    /(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})/,
                                    "$1-$2-$3T$4:$5:$6"
                                ))
                        }
                        
                        return {
                            id: crypto.randomUUID(),
                            calendarId: '1',
                            title: summary,
                            category: 'time',
                            start: formatDate(dtstart),
                            end: formatDate(dtend),
                            body: description,
                            location: location,
                        };
                    });
                    console.log(events);
                    calendar.createEvents(events);
                })
                .catch(error => console.error('Error fetching calendar data:', error));
        });
    </script>
<?php $t->endSlot(); ?>