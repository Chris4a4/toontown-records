<script>
  import DiscordLogin from '$lib/components/DiscordLogin.svelte';
  const navItems = [
    { icon: '🔥', text: 'Records', href: '/records' },
    { icon: '🏆', text: 'Leaderboard', href: '/leaderboards' },
    { icon: '👤', text: 'Rules', href: '/rules' },
    { icon: 'ℹ️', text: 'About', href: '/about' }
  ];
</script>

<nav class="bg-[#D5C5C8] text-black p-4 flex justify-between items-center">
  <h1 class="text-xl font-bold mr-6">
    <a href='/'>
      Toontown Records
    </a>
  </h1>

  <div class="flex items-center">
    <ul class="flex space-x-6">
      {#each navItems as item}
        <li>
          <a href={item.href} class="flex items-center hover:text-gray-300">
            <span class="mr-1">{item.icon}</span>
            <span>{item.text}</span>
          </a>
        </li>
      {/each}
    </ul>
  </div>
  <DiscordLogin />
</nav>

<div class="bg-blue-400 h-1"></div>