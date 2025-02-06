function datePicker() {
  return {
    startDate: "",
    endDate: "",
    calendarInstance: null,
    calendarVisible: false, // Set to false to ensure calendar is hidden by default

    init() {
      this.calendarInstance = flatpickr("#flatpickr-calendar", {
        inline: true,
        mode: "range",
        dateFormat: "Y-m-d",
        onChange: (selectedDates) => {
          if (selectedDates.length === 2) {
            this.startDate = flatpickr.formatDate(selectedDates[0], "Y-m-d");
            this.endDate = flatpickr.formatDate(selectedDates[1], "Y-m-d");
          } else if (selectedDates.length === 1) {
            this.startDate = flatpickr.formatDate(selectedDates[0], "Y-m-d");
            this.endDate = ""; // Reset end date if only one date is selected
          }
        },
      });

      // Ensure calendar stays open when clicking inside
      document.addEventListener("click", (event) => {
        const isClickInside =
          document
            .querySelector("#flatpickr-calendar")
            .contains(event.target) ||
          document.querySelector("[x-data]").contains(event.target);

        if (!isClickInside) {
          this.hideCalendar();
        }
      });

      // Add event listener for the "Clear all" button
      document.getElementById("clearButton").addEventListener("click", () => {
        this.clearAll();
      });
    },

    showCalendar() {
      this.calendarVisible = true;
      document.querySelector("#flatpickr-calendar").style.display = "block";
    },

    hideCalendar() {
      this.calendarVisible = false;
      document.querySelector("#flatpickr-calendar").style.display = "none";
    },

    setPredefinedDates(option) {
      const today = new Date();
      let start, end;

      switch (option) {
        case "yesterday":
          end = new Date(today);
          start = new Date(today);
          start.setDate(today.getDate() - 1);
          break;
        case "last7days":
          end = new Date(today);
          start = new Date(today);
          start.setDate(today.getDate() - 7);
          break;
        case "last15days":
          end = new Date(today);
          start = new Date(today);
          start.setDate(today.getDate() - 15);
          break;
        case "last30days":
          end = new Date(today);
          start = new Date(today);
          start.setDate(today.getDate() - 30);
          break;
        case "last3months":
          end = new Date(today);
          start = new Date(today);
          start.setMonth(today.getMonth() - 3);
          break;
      }

      this.startDate = flatpickr.formatDate(start, "Y-m-d");
      this.endDate = flatpickr.formatDate(end, "Y-m-d");

      if (this.calendarInstance) {
        this.calendarInstance.setDate([start, end]);
        this.calendarInstance.jumpToDate(start);
      }

      // Keep the calendar open after selecting a predefined range
      this.showCalendar();
    },

    clearAll() {
      // Clear start and end dates
      this.startDate = "";
      this.endDate = "";

      // Clear the calendar instance's dates
      if (this.calendarInstance) {
        this.calendarInstance.clear();
      }

      // Optionally, keep the calendar visible or hide it
      this.showCalendar();
    },
  };
}

document.addEventListener("alpine:init", () => {
  Alpine.data("datePicker", datePicker);
});
