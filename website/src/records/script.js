let numDummyItems = 30;

// Create loading icons
window.addEventListener("DOMContentLoaded", () => {
  for (let i = 0; i < numDummyItems; i++) {
    document
      .getElementById("record-container")
      .insertAdjacentHTML("beforeend", make_placeholder(i));
  }
});

// Populate records
window.addEventListener("load", () => {
  fetch("/api/leaderboards/records")
    .then((response) => response.json())
    .then((data) => {
      for (let i = 0; i < data.length; i++) {
        if (i < numDummyItems) {
          document.getElementById(`record-${i}`).outerHTML = make_record(
            i,
            data[i]["record_name"],
            data[i]["tags"],
            data[i]["value"],
            data[i]["submitters"],
          );
        } else {
          document
            .getElementById("record-container")
            .insertAdjacentHTML(
              "beforeend",
              make_record(
                i,
                data[i]["record_name"],
                data[i]["tags"],
                data[i]["value"],
                data[i]["submitters"],
              ),
            );
        }
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
});

function make_placeholder(i) {
  return /* HTML */ `
    <li
      id="record-${i}"
      class="h-[220px] w-[380px] overflow-hidden rounded-lg bg-[url(/images/unknown.webp)]"
    ></li>
  `;
}

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
      class="${bgImage} h-[220px] w-[380px] overflow-hidden rounded-lg"
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
