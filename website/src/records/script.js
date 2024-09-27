// Populate records
window.addEventListener("load", () => {
  fetch("/api/leaderboards/grouped_records")
    .then((response) => response.json())
    .then((data) => {
      Object.keys(data).forEach((key) => {
        // Create title
        document
        .getElementById("record-container")
        .insertAdjacentHTML(
          "beforeend",
          `<h1 class="text-white font-poppins font-extrabold text-5xl pt-8 pb-2 drop-shadow-2xl">${key}</h1>`
        );

        // Create records
        let r = '<ul class="flex flex-grid flex-wrap">';
        for (let i = 0; i < data[key].length; i++){
            r += make_record(
                i,
                data[key][i]["record_name"],
                data[key][i]["tags"],
                data[key][i]["value"],
                data[key][i]["submitters"],
              )
        }
        r += '</ul>';

        console.log(r);

        document
        .getElementById("record-container")
        .insertAdjacentHTML(
          "beforeend",
          r
        );
      });
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
});

function make_record(i, recordName, tags, value, submitters) {
  if (value === null) {
    value = "N/A";
  }

  let gameImageAlt = "???";
  let gameImagePath = "???";
  if (tags.includes("ttr")) {
    gameImageAlt = "Toontown Rewritten logo";
    gameImagePath = "/images/ttr_smaller.webp";
  } else if (tags.includes("ttcc")) {
    gameImageAlt = "Corporate Clash logo";
    gameImagePath = "/images/ttcc.webp";
  }

  let bgImage = "???";
  if (tags.includes("vp")) {
    bgImage = "bg-[url(/images/records/vp.webp)]";
  } else if (tags.includes("cfo")) {
    bgImage = "bg-[url(/images/records/cfo.webp)]";
  } else if (tags.includes("cj")) {
    bgImage = "bg-[url(/images/records/cj.webp)]";
  } else if (tags.includes("ceo")) {
    bgImage = "bg-[url(/images/records/ceo.webp)]";
  }

  let bgColor = "bg-black";
  if (tags.includes("rl")) {
    bgColor = "bg-rloverlay";
  }

  let submittersSize = "text-2xl";
  if (submitters.length > 100) {
    submittersSize = "text-sm";
  } else if (submitters.length > 50) {
    submittersSize = "text-base";
  }

  return /* HTML */ `
    <li
      id="record-${i}"
      class="${bgImage} h-[220px] w-[380px] overflow-hidden rounded-lg m-4"
    >
      <div class="${bgColor} h-full w-full p-2 text-white opacity-75">
        <div class="flex h-2/5 justify-between">
          <h1 class="font-poppins text-xl font-extrabold">
            ${recordName.toUpperCase()}
          </h1>
          <img
            alt="${gameImageAlt}"
            src="${gameImagePath}"
            class="h-[54px] w-[54px]"
          />
        </div>
        <p class="font-poppins text-3xl font-extrabold">${value}</p>
        <div class="flex h-1/2 items-center">
          <p class="${submittersSize} font-poppins font-semibold">
            ${submitters}
          </p>
        </div>
      </div>
    </li>
  `;
}
