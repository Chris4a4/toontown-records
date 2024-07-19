<script>
  import DiscordLogin from '$lib/components/DiscordLogin.svelte';
  import logo from '$lib/assets/logo.png';
  import { page } from '$app/stores';

  const navItems = [
    { text: 'Records', href: '/records' },
    { text: 'Leaderboard', href: '/leaderboards' },
    { text: 'Rules', href: '/rules' },
    { text: 'About', href: '/about' }
  ];
</script>

<nav class="bg-lightpink flex justify-between items-center">
  <div class="w-40 p-2">
    <a href='/'>
      <img alt="Toontown Records logo" src={logo} />
    </a>
  </div>

  <div>
    <ul class="flex text-royalblue font-minnie sm:text-lg md:text-xl lg:text-2xl xl:text-3xl sm:space-x-2 md:space-x-6 lg:space-x-10 xl:space-x-14">
      {#each navItems as item}
        <a href={item.href}>
          <li class="relative group">
            <span class="group-hover:text-raisinblack">
              {item.text}
            </span>
            {#if $page.url.pathname === item.href}
              <div class="w-full h-1 bg-current group-hover:bg-raisinblack"></div>
            {:else}
              <div class="w-full h-1 bg-lightpink"></div>
            {/if}
          </li>
        </a>
      {/each}
    </ul>
  </div>
  <div class="p-2">
    <DiscordLogin />
  </div>
</nav>

<div class="bg-raisinblack h-1"></div>
