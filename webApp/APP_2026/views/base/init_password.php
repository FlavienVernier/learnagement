<?php $t->extend('layouts/base'); ?>

<?php $t->startSlot('title'); ?>Mot de passe — Learnagement<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>
  <div class="flex grow items-center justify-center">

    <!-- Carte formulaire -->
    <div class="rounded-2xl shadow-lg p-8 w-[75%]">
      <form action="<?= $t->router->href('inscription-post') ?>" method="POST" class="space-y-5">
        <input type='hidden' name='email' value='<?= $email ?>'>
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

        <!-- Mot de passe -->
        <div>
          <label for="confirm" class="block mb-2 text-sm font-medium text-gray-700">
            Confirmer le mot de passe
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
              id="confirm"
              name="confirm"
              required
              placeholder="••••••••"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-xl focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-3"
            />
          </div>
        </div>

        <!-- Bouton de connexion -->
        <button type="submit" class="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-semibold rounded-xl text-sm px-5 py-3 text-center transition-colors duration-200">
          Se connecter
        </button>

      </form>
    </div>

  </div>
<?php $t->endSlot(); ?>