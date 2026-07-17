<?php $t->extend('layouts/base'); ?>

<?php $t->startSlot('title'); ?>Connexion — Learnagement<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>
  <div class="flex grow items-center justify-center">

    <!-- Carte formulaire -->
    <div class="rounded-2xl shadow-lg p-8 w-[75%]">
        <hr>
        <label for="email" class="block mb-2 text-sm font-medium text-gray-700 text-center">
            <i> Login USMB</i>
        </label>
        <!-- Bouton de connexion CAS -->
        <div class="flex items-center justify-center mt-4">
            <a href="<?= getenv("CAS_HOST") . "/login?service=" . urlencode(getenv("FRONT_PHP_PROTOCOL") . "://" . getenv("INSTANCE_URL") . "/") ?>"
               class="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-semibold rounded-xl text-sm px-5 py-3 text-center transition-colors duration-200">
                Se connecter / avec CAS - USMB
            </a>
        </div>
        <div>
            <br>
            <hr>
            <label for="email" class="block mb-2 text-sm font-medium text-gray-700 text-center">
               <i> ou en local</i>
            </label>
        </div>
      <form action="<?= $t->router->href('login-post') ?>" method="POST" class="space-y-5">

        <!-- Email -->
        <div>
          <label for="email" class="block mb-2 text-sm font-medium text-gray-700">
            Adresse e-mail
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
            </div>
            <input
              type="email"
              id="email"
              name="email"
              required
              placeholder="nom@exemple.com"
              class="border border-gray-300 text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-3"
            />
          </div>
        </div>

        <!-- Mot de passe -->
        <div>
          <label for="password" class="block mb-2 text-sm font-medium text-gray-700">
            Mot de passe
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
            <input
              type="password"
              id="password"
              name="password"
              required
              placeholder="••••••••"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-3"
            />
          </div>
        </div>

        <!-- Options : se souvenir / mot de passe oublié -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember"
              type="checkbox"
              class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300"
            />
            <label for="remember" class="ml-2 text-sm text-gray-600">
              Se souvenir de moi
            </label>
          </div>
          <a href="#" class="text-sm font-medium text-blue-600 hover:underline">
            Mot de passe oublié ?
          </a>
        </div>

        <!-- Bouton de connexion -->
        <button type="submit" class="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-semibold rounded-xl text-sm px-5 py-3 text-center transition-colors duration-200">
          Se connecter / avec un compte local
        </button>

      </form>
    </div>


<?php $t->endSlot(); ?>