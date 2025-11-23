<form method="post" action="?page=check_mdp" 
      class="flex flex-col justify-center grow px-4 py-8 max-w-md mx-auto w-full">

  <div class="space-y-6">

    <!-- Adresse mail -->
    <div>
      <label for="id" class="block text-sm font-medium text-gray-900">Adresse mail</label>
      <div class="mt-2">
        <input
          id="id"
          type="text"
          name="id"
          placeholder="john.doe@etu.univ-savoie.fr"
          class="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary sm:text-sm"
          required
        />
      </div>
    </div>

    <!-- Mot de passe -->
    <div>
      <label for="mdp" class="block text-sm font-medium text-gray-900">Mot de passe</label>
      <div class="mt-2">
        <input
          id="mdp"
          type="password"
          name="mdp"
          placeholder="********"
          class="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary sm:text-sm"
          required
        />
      </div>
    </div>

  </div>

  <!-- Bouton -->
  <div class="mt-8">
    <button
      type="submit"
      name="inscription_ok"
      value="Popup"
      class="w-full rounded-lg bg-primary text-on-primary px-4 py-2 font-semibold shadow hover:opacity-90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
    >
      Connexion
    </button>
  </div>

</form>
