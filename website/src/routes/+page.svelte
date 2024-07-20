<script>
  import logo from '$lib/assets/logo.png';
  import { fade } from 'svelte/transition';

  import Slide0 from '$lib/components/homeCarousel/Slide0.svelte';
  import Slide1 from '$lib/components/homeCarousel/Slide1.svelte';
  import Slide2 from '$lib/components/homeCarousel/Slide2.svelte';
  import Slide3 from '$lib/components/homeCarousel/Slide3.svelte';
  import Slide4 from '$lib/components/homeCarousel/Slide4.svelte';

  let currentSlide = 0;
  const slides = [
    {color: 'bg-emeraldgreen', slide: Slide0},
    {color: 'bg-royalblue', slide: Slide1},
    {color: 'bg-lightpink', slide: Slide2},
    {color: 'bg-raisinblack', slide: Slide3},
    {color: 'bg-[#858FFF]', slide: Slide4}
  ];

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
  }

  function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
  }
</script>

<main class="bg-custom-background bg-cover bg-center min-h-screen">
  <!-- Logo -->
  <div class="flex justify-center items-center">
    <img alt="Toontown Records logo"
         src={logo}
         class="w-full md:w-3/4 max-w-3xl custom-drop-shadow p-20"
    />
  </div>

  <!-- Carousel -->
  <div class="relative w-full h-[38rem] sm:h-[32rem] md:h-[26rem] lg:h-96 xl:h-80 bg-teal-200 focused-drop-shadow">
    <!-- Content -->
    <div class="absolute inset-0 py-4 px-12 {slides[currentSlide].color} flex justify-center" transition:fade>
      <svelte:component this={slides[currentSlide].slide} />
    </div>
    
    <!-- Navigation Buttons -->
    <button on:click={prevSlide} class="absolute left-2 top-1/2 transform -translate-y-1/2" aria-label="Previous slide">
      <svg xmlns="http://www.w3.org/2000/svg" class="arrow-svg" fill="none" viewBox="0 0 24 24" stroke="white">
        <path stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <button on:click={nextSlide} class="absolute right-2 top-1/2 transform -translate-y-1/2" aria-label="Next slide">
      <svg xmlns="http://www.w3.org/2000/svg" class="arrow-svg" fill="none" viewBox="0 0 24 24" stroke="white">
        <path stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
    
    <!-- Navigation Dots -->
    <div class="absolute bottom-2 left-1/2 transform -translate-x-1/2 flex space-x-4">
      {#each slides as _, i}
        <div class={`w-4 h-4 rounded-full bg-white ${i === currentSlide ? '' : 'bg-opacity-20'}`}></div>
      {/each}
    </div>
  </div>
</main>

<style>
  .custom-drop-shadow {
    filter: drop-shadow(0 0 50px theme('colors.lightpink'));
  }
  .focused-drop-shadow {
    filter:
      drop-shadow(0 0 10px theme('colors.lightpink'))
      drop-shadow(0 0 10px theme('colors.lightpink'));
  }

  .arrow-svg {
    width: calc(24px + 2vw);
    height: calc(24px + 2vw);
    min-width: 24px;
    min-height: 24px;
    max-width: 64px;
    max-height: 64px;
  }
</style>