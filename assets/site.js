// Ketut Bali Private Driver — booking form → WhatsApp deep link
(function () {
  var WA_NUMBER = "6281805568096";

  var form = document.getElementById("bookingForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var get = function (id) {
        var el = document.getElementById(id);
        return el && el.value ? el.value.trim() : "";
      };
      var lang = document.documentElement.lang === "fr" ? "fr" : "en";
      var lines =
        lang === "fr"
          ? [
              "Bonjour Ketut ! Je souhaite réserver un chauffeur à Bali.",
              "• Nom : " + get("bf-name"),
              "• Date : " + get("bf-date"),
              "• Personnes : " + get("bf-pax"),
              "• Prise en charge : " + (get("bf-pickup") || "à confirmer"),
              "• Service : " + get("bf-service"),
            ]
          : [
              "Hi Ketut! I'd like to book a driver in Bali.",
              "• Name: " + get("bf-name"),
              "• Date: " + get("bf-date"),
              "• People: " + get("bf-pax"),
              "• Pickup: " + (get("bf-pickup") || "to be confirmed"),
              "• Service: " + get("bf-service"),
            ];
      var extra = get("bf-msg");
      if (extra) lines.push((lang === "fr" ? "• Détails : " : "• Details: ") + extra);
      var url =
        "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(lines.join("\n"));
      window.open(url, "_blank", "noopener");
    });
  }

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
