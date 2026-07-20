// Ketut Bali Private Driver — booking form → WhatsApp deep link
(function () {
  var WA_NUMBER = "6281805568096";

  var I18N = {
    en: {
      intro: "Hi Ketut! I'd like to book a driver in Bali.",
      name: "Name", date: "Date", pax: "People", pickup: "Pickup",
      service: "Service", details: "Details", tbc: "to be confirmed"
    },
    fr: {
      intro: "Bonjour Ketut ! Je souhaite réserver un chauffeur à Bali.",
      name: "Nom", date: "Date", pax: "Personnes", pickup: "Prise en charge",
      service: "Service", details: "Détails", tbc: "à confirmer"
    },
    de: {
      intro: "Hallo Ketut! Ich möchte einen Fahrer auf Bali buchen.",
      name: "Name", date: "Datum", pax: "Personen", pickup: "Abholort",
      service: "Leistung", details: "Details", tbc: "noch offen"
    },
    ru: {
      intro: "Здравствуйте, Кетут! Я хочу заказать водителя на Бали.",
      name: "Имя", date: "Дата", pax: "Человек", pickup: "Место подачи",
      service: "Услуга", details: "Детали", tbc: "уточним"
    },
    zh: {
      intro: "您好Ketut！我想在巴厘岛预订司机。",
      name: "姓名", date: "日期", pax: "人数", pickup: "接载地点",
      service: "服务", details: "备注", tbc: "待确认"
    }
  };

  var form = document.getElementById("bookingForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var get = function (id) {
        var el = document.getElementById(id);
        return el && el.value ? el.value.trim() : "";
      };
      var t = I18N[document.documentElement.lang] || I18N.en;
      var lines = [
        t.intro,
        "• " + t.name + ": " + get("bf-name"),
        "• " + t.date + ": " + get("bf-date"),
        "• " + t.pax + ": " + get("bf-pax"),
        "• " + t.pickup + ": " + (get("bf-pickup") || t.tbc),
        "• " + t.service + ": " + get("bf-service")
      ];
      var extra = get("bf-msg");
      if (extra) lines.push("• " + t.details + ": " + extra);
      var url = "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(lines.join("\n"));
      window.open(url, "_blank", "noopener");
    });
  }

  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
