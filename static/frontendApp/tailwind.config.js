/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./**/*.html", "./src/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        inter: ["inter"],
        manrope: ["manrope"],
        poppins: ["Poppins", "sans-serif"],
      },
      colors: {
        "light-blue": "#EDECFC",
        "custom-blue": "#5694D9",
        "custom-violate": "#9F5ABA",
        "custom-green": "#138174",
        "custom-orange": "#E3985C",
        "custom-dark-blue": "#4F46E5",
        "custom-black": "#101929",
        "aws-color": "#FF9900",
        "azure-color": "#035BDA",
        "claude-color": "#D97757",
      },
      width: {
        34: "34px", // Custom width for 34px
      },
      fontSize: {
        "cus-10px": "10px", // Custom font size for 10px
      },
      margin: {
        "32px": "32px",
      },
      appearance: {
        none: "-webkit-appearance:none; -moz-appearance:none; appearance:none;", //Support mac book select or any options
      },
    },
  },
  plugins: [],
};
