tailwind.config = {
  content: ["./*.html"],
  theme: {
    colors: {
      primary: "#111826",
      lightred: "#FBD5D5",
      white:"#fff",
    },
    extend: {
      fontSize: {
        //font-size and line-height used
        textdetails: ["16px", "29px"],
        //font-size and line-height and letter-spacing font-weight combined
        h1: [
          "42px",
          {
            lineHeight: "46px",
            letterSpacing: "1px",
            fontWeight: "500",
          },
        ],
      },
      letterSpacing: {
        1: "0.16px",
        2: "0.32px",
      },
      screens: {
        sm: "576px",
        sm: { max: "767px" },
        mdscreen: { min: "768px" },
        md: { min: "768px", max: "991px" },
        lg: { min: "992px", max: "1199px" },
        xl: { min: "1200px", max: "1399px" },
        xxl: { min: "1400px" },
      },
      container: {
        center: true,
        screens: {
          sm: { max: "767px" },
          md: { min: "768px", max: "991px" },
          lg: { min: "992px", max: "1199px" },
          xl: { min: "1200px", max: "1399px" },
          xxl: { min: "1400px" },
        },
      },
      spacing: {},
      padding: {
        screen: "0px 12px",
      },
      margin: {
        screen: "0px -12px",
      },
    },
  },
};