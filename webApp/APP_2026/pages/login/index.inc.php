<form method="post" action="?page=check_password" 
      class="flex flex-col justify-center grow px-4 py-8 max-w-md mx-auto w-full">

  <div class="space-y-6">

    <!-- Adresse mail -->
    <div>
      <label for="email" class="block text-sm font-medium text-gray-900">Adresse mail</label>
      <div class="mt-2">
        <input
          type="email"
          name="email"
          placeholder="john.doe@etu.univ-savoie.fr"
          class="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary sm:text-sm"
          required
        />
      </div>
    </div>

    <!-- Mot de passe -->
    <div>
      <label for="password" class="block text-sm font-medium text-gray-900">Mot de passe</label>
      <div class="mt-2">
        <input
          type="password"
          name="password"
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
      class="w-full rounded-lg bg-primary text-on-primary px-4 py-2 font-semibold shadow hover:opacity-90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
    >
      Connexion
    </button>
  </div>

</form>
