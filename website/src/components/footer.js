window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("footer").outerHTML = /* HTML */ `
    <footer id="footer" class="flex flex-col items-center bg-gunmetal">
      <div class="m-8 grid max-w-screen-xl grid-cols-5 gap-10">
        <p class="font-lexend text-xl text-white">
          Toontown Records is your go-to hub for tracking records and preserving
          the top toons’ remarkble feats.
        </p>
        <div class="flex flex-col items-center">
          <h1 class="mb-10 font-fredoka text-2xl text-white underline">
            Contact Us
          </h1>

          <div class="flex w-3/4 justify-between">
            <img
              alt="Discord Icon"
              src="/images/discord_icon.webp"
              class=""
            />
            <img
              alt="Mail Icon"
              src="/images/mail_icon.webp"
              class=""
            />
          </div>
        </div>
        <img
          alt="Toontown Records logo"
          src="/images/logo_full.webp"
          class="w-full"
        />
        <div class="flex flex-col items-center">
          <h1 class="mb-10 font-fredoka text-2xl text-white underline">
            Supported Games
          </h1>

          <div class="flex w-full justify-between">
            <img alt="Corporate Clash logo" src="/images/ttcc.webp" class="" />
            <img
              alt="Toontown Rewritten logo"
              src="/images/ttr.webp"
              class=""
            />
          </div>
        </div>
        <ul class="font-poppins text-2xl font-black text-white">
          <li>ABOUT</li>
          <li>FAQ</li>
          <li>PRIVACY POLICY</li>
          <li>TERMS OF SERVICE</li>
        </ul>
      </div>
      <h1
        class="mb-8 max-w-screen-2xl text-center font-lexend text-2xl text-white"
      >
        Toontown Records is not affiliated with Walt Disney Company, and/or
        Disney Interactive. Toontown Records is also not affiliated with
        Toontown Rewritten and Corporate Clash.
      </h1>
    </footer>
  `;
});
