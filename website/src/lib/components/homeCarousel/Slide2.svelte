<script>
  import chrisAvatar from '$lib/assets/chrisAvatar.png';
  import louAvatar from '$lib/assets/louAvatar.png';
</script>

<div class="max-w-3xl font-righteous text-raisinblack">
  <h2 class="text-5xl text-center drop-shadow-lg">Meet The Staff Members</h2>
  <div class="h-1 w-full m-2 mb-4 bg-royalblue"></div>

  <div class="flex items-center justify-center p-4">
    <div class="text-4xl text-center block sm:hidden drop-shadow-lg">PROJECT MANAGERS</div>
  </div>

  <div class="w-full flex justify-evenly">

    <div class="flex flex-col items-center">
      <img alt="Chris4a4's avatar"
        src={chrisAvatar}
        class="w-full md:w-2/3 lg:w-1/2"
      />
      <span class="text-royalblue text-3xl md:pt-2">Chris4a4</span>
      <span class="text-raisinblack text-xl">Lead Developer</span>
    </div>

    <div class="flex items-center justify-center p-4">
      <div class="text-2xl sm:text-3xl md:text-5xl text-center hidden sm:block drop-shadow-lg">PROJECT MANAGERS</div>
    </div>

    <div class="flex flex-col items-center">
      <img alt="Kitt Kitt Lou's avatar"
        src={louAvatar}
        class="w-full md:w-2/3 lg:w-1/2"
      />
      <span class="text-royalblue text-3xl md:pt-2">Kitt Kitt Lou</span>
      <span class="text-raisinblack text-xl">Lead Director</span>
    </div>
  </div>
</div>