<script>
  import { slide } from 'svelte/transition';
  import DiscordLogin from '$lib/components/DiscordLogin.svelte';
  import logo_small from '$lib/assets/logo_small.png';
  import { page } from '$app/stores';
  import { discordAvatar } from '$lib/stores.js'

  let isMobileMenuOpen = false;
  const navItems = [
    { text: 'Records', href: '/records' },
    { text: 'Leaderboard', href: '/leaderboards' },
    { text: 'Rules', href: '/rules' },
    { text: 'News', href: '/news' }
  ];

  function toggleMobileMenu() {
    isMobileMenuOpen = !isMobileMenuOpen;
  }
</script>

<div class="bg-gunmetal">
  <nav class="bg-gunmetal h-20 flex justify-between items-center max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Logo -->
    <div class="p-2 flex-shrink-0 drop-shadow-lg">
      <a href='/' class="btn-animate block w-full h-full">
        <img alt="Toontown Records logo" src={logo_small} class="w-full h-full" />
      </a>
    </div>

    <!-- Desktop menu -->
    <div class="flex-grow hidden xl:block">
      <ul class="flex justify-center text-white font-minnie text-3xl space-x-14">
        {#each navItems as item}
          <a href={item.href}>
            <li class="btn-animate relative group">
              <span class="group-hover:text-frenchgray">
                <div class="drop-shadow-lg">{item.text}</div>
              </span>
              {#if $page.url.pathname === item.href}
                <div class="w-full h-1 bg-current group-hover:bg-frenchgray drop-shadow-lg"></div>
              {:else}
                <div class="w-full h-1 bg-gunmetal"></div>
              {/if}
            </li>
          </a>
        {/each}
      </ul>
    </div>

    <!-- User profile section -->
    {#if $discordAvatar}
      <img src={$discordAvatar} alt="Discord Avatar" class="max-h-16 rounded-full" />
    {:else}
      <DiscordLogin/>
    {/if}

    <!-- Dropdown button for mobile -->
    <button 
      class="xl:hidden p-1 drop-shadow-lg hover:bg-frenchgray outline-white rounded-sm outline outline-2 btn-animate text-white text-2xl"
      on:click={toggleMobileMenu}
      aria-label="Toggle mobile menu"
    >
      ☰
    </button>
  </nav>
</div>

<!-- Mobile menu -->
{#if isMobileMenuOpen}
  <div transition:slide="{{ duration: 300, axis: 'y' }}" class="bg-gunmetal xl:hidden">
    <ul class="flex flex-col text-royalblue font-minnie text-2xl">
      {#each navItems as item}
        <a href={item.href}>
          <li class="btn-animate p-2 relative group">
            <span class="group-hover:text-frenchgray inline-block">
              <div class="drop-shadow-lg">{item.text}</div>
              {#if $page.url.pathname === item.href}
                <div class="w-full h-1 drop-shadow-lg bg-current group-hover:bg-frenchgray"></div>
              {:else}
                <div class="w-full h-1 bg-gunmetal"></div>
              {/if}
            </span>
          </li>
        </a>
      {/each}
    </ul>
  </div>
{/if}
