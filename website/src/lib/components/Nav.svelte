<script>
  import { slide } from 'svelte/transition';
  import DiscordLogin from '$lib/components/DiscordLogin.svelte';
  import logo from '$lib/assets/logo.png';
  import { page } from '$app/stores';

  let isMobileMenuOpen = false;
  const navItems = [
    { text: 'Records', href: '/records' },
    { text: 'Leaderboard', href: '/leaderboards' },
    { text: 'Rules', href: '/rules' },
    { text: 'About', href: '/about' }
  ];

  function toggleMobileMenu() {
    isMobileMenuOpen = !isMobileMenuOpen;
  }
</script>

<div class="bg-lightpink">
  <nav class="bg-lightpink flex justify-between items-center max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Logo -->
    <div class="w-40 p-2 flex-shrink-0 drop-shadow-lg">
      <a href='/' class="btn-animate block w-full h-full">
        <img alt="Toontown Records logo" src={logo} class="w-full h-full" />
      </a>
    </div>
  
    <!-- Dropdown button for mobile -->
    <button 
      class="xl:hidden p-1 drop-shadow-lg hover:bg-emeraldgreen outline-royalblue rounded-sm outline outline-2 btn-animate text-royalblue text-2xl"
      on:click={toggleMobileMenu}
      aria-label="Toggle mobile menu"
    >
      ☰
    </button>
  
    <!-- Desktop menu -->
    <div class="flex-grow hidden xl:block">
      <ul class="flex justify-center text-royalblue font-minnie text-3xl space-x-14">
        {#each navItems as item}
          <a href={item.href}>
            <li class="btn-animate relative group">
              <span class="group-hover:text-raisinblack">
                <div class="drop-shadow-lg">{item.text}</div>
              </span>
              {#if $page.url.pathname === item.href}
                <div class="w-full h-1 bg-current group-hover:bg-raisinblack drop-shadow-lg"></div>
              {:else}
                <div class="w-full h-1 bg-lightpink"></div>
              {/if}
            </li>
          </a>
        {/each}
      </ul>
    </div>
  
    <!-- Connect with Discord button -->
    <DiscordLogin/>
  </nav>
</div>

<div class="bg-raisinblack h-1"></div>

<!-- Mobile menu -->
{#if isMobileMenuOpen}
  <div transition:slide="{{ duration: 300, axis: 'y' }}" class="bg-lightpink xl:hidden">
    <ul class="flex flex-col text-royalblue font-minnie text-2xl">
      {#each navItems as item}
        <a href={item.href}>
          <li class="btn-animate p-2 relative group">
            <span class="group-hover:text-raisinblack inline-block">
              <div class="drop-shadow-lg">{item.text}</div>
              {#if $page.url.pathname === item.href}
                <div class="w-full h-1 drop-shadow-lg bg-current group-hover:bg-raisinblack"></div>
              {:else}
                <div class="w-full h-1 bg-lightpink"></div>
              {/if}
            </span>
          </li>
        </a>
      {/each}
    </ul>
  </div>
  <div class="xl:hidden bg-raisinblack h-1"></div>
{/if}