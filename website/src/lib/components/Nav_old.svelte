<script>
  import { page } from '$app/stores';
</script>
  
<nav>
  <ul>
    <li class:active={$page.url.pathname === '/'}>
      <a href="/">Home</a>
    </li>
    <li class:active={$page.url.pathname === '/records'}>
      <a href="/records">Records</a>
    </li>
    <li class:active={$page.url.pathname === '/leaderboards'}>
      <a href="/leaderboards">Leaderboards</a>
    </li>
    <li class:active={$page.url.pathname === '/rules'}>
      <a href="/rules">Rules</a>
    </li>
    <li class:active={$page.url.pathname === '/about'}>
      <a href="/about">About</a>
    </li>
  </ul>
</nav>

<style>
  nav {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 1rem;
  }

  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    display: flex;
    justify-content: space-around;
  }

  li {
    display: inline;
  }

  a {
    text-decoration: none;
    color: #333;
    font-weight: bold;
  }

  .active a {
    color: #007bff;
  }
</style>