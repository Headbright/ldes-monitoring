import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "LDES Dashboard",
  description: "LDES Overview and status",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: "/logo.svg",
    nav: [{ text: "Home", link: "/" }],
    outline: false,
    sidebar: [
      {
        text: "Streams",
        items: [{ text: "IoW", link: "/dashboard" }],
      },
    ],

    // default value is true. Set it to false to hide next page links on all pages
    nextLinks: false,
    // default value is true. Set it to false to hide prev page links on all pages
    prevLinks: false,

    socialLinks: [
      { icon: "github", link: "https://github.com/Headbright/ldes-monitoring" },
    ],
  },
});
